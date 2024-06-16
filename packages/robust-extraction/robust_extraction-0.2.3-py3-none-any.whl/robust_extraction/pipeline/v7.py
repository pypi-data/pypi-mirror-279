from dataclasses import dataclass
import haskellian.either as E
import cv2 as cv
import numpy as np
import ramda as R
import pure_cv as vc
from .ret import Result, NotEnoughCols, NotEnoughRows, UnkownError, Ok
from .. import contours as cs, templates as ts, lines as ls, perspective as pve, match1d

def descaled_extract(
  img: cv.Mat, model: ts.SheetModel,
  min_height_p = 0.8, min_width_p = 0.8,
  filter_row_coverage = True, filter_col_coverage = True,
  verbose = False, auto_h: int | None = 1080, descale_h: int | None = 1920,
  logger = None, autocorrect = True
) -> Result:
  """Like `v6` but descaling and rescaling"""
  try:
    if autocorrect:
      big_corr, perspective_corners = pve.descaled_autocorrect(img, model, pve.Params(rescale_h=auto_h), logger=logger)
    else:
      big_corr = img
      perspective_corners = None
    corr_img = vc.descale_h(big_corr, descale_h) if descale_h is not None else big_corr
    scale = big_corr.shape[0] / corr_img.shape[0]
    height, width = corr_img.shape[:2]
    MIN_ROW_H = min_height_p*height*model.rmin
    MIN_COL_W = min_width_p*width*model.cmin
    cnt = cs.padded_grid(corr_img, cs.Params(pad_h_prop=model.rmin, pad_v_prop=model.cmin))
    all_lines = ls.find(corr_img)
    lines = np.int32([
      cropped for line in all_lines
        if (cropped := ls.crop(line, box=cnt)) is not None
    ])
    vlines, hlines = ls.cluster.vh(lines)
    
    min_rows = model.rows.b - model.rows.a
    rows = ls.cluster.collinear.adaptive_cluster(
      lines=hlines, min_d=MIN_ROW_H, min_clusters=min_rows,
      size=height, inclination="horizontal", n_iters=100, verbose=verbose
    )
    if filter_row_coverage:
      filtered_rows = ls.coverage.filter(rows, axis=0, k=2)
      inlier_rows = rows if len(filtered_rows) < min_rows else filtered_rows
    else:
      inlier_rows = rows
    if len(inlier_rows) < min_rows:
      return E.Left(NotEnoughRows(detected=len(inlier_rows), required=min_rows))
    imp_rows = match1d.invariant(clusters=inlier_rows, template=model.rows, inclination='rows')
    
    min_cols = model.cols.b - model.cols.a
    cols = ls.cluster.collinear.cluster(
      lines=vlines, threshold=0.5*MIN_COL_W,
      size=width, inclination="vertical"
    )
    if filter_col_coverage:
      filtered_cols = ls.coverage.filter(cols, axis=1)
      inlier_cols = cols if len(filtered_cols) < min_cols else filtered_cols
    else:
      inlier_cols = cols
    if len(inlier_cols) < min_cols:
      return E.Left(NotEnoughCols(detected=len(inlier_cols), required=min_cols))
    imp_cols = match1d.invariant(clusters=inlier_cols, template=model.cols, inclination='cols')
    poly_rows = R.map(ls.poly.hfit(xmin=0, xmax=width), imp_rows)
    poly_cols = R.map(ls.poly.vfit(ymin=0, ymax=height), imp_cols)
    xs = ls.poly.intersect_all(poly_rows, poly_cols)
    contours = np.int32(scale * ts.contours(model, xs.get))
    boxes = R.map(cs.roi(img=big_corr), contours)
    return E.Right(Ok(corr_img=big_corr, boxes=boxes, contours=contours, perspective_corners=perspective_corners))
  except Exception as e:
    return E.Left(UnkownError(detail=str(e)))
