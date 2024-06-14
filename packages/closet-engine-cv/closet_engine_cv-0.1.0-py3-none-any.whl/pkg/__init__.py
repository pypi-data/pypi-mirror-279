import argparse
import cv2
import os
from os.path import join, getsize, basename, splitext
import numpy as np

def compare(x_path, y_path):
    x = cv2.imread(x_path)
    y = cv2.imread(y_path)
    diff = cv2.absdiff(x, y)
    res, thres_diff = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY)

    def make_morphed():
        kernel = np.ones((3,3),np.uint8)
        openingDiff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernel)
        res, out = cv2.threshold(openingDiff, 10, 255, cv2.THRESH_BINARY)
        return out
    
    morphed = make_morphed()
    combined = np.concatenate((x, y, diff, thres_diff, morphed), axis=1)

    return (x, y, diff, thres_diff, morphed, combined)

def main():
    parser = argparse.ArgumentParser(description='Generate diff images')
    parser.add_argument('-x', nargs=1, type=str, required=True)
    parser.add_argument('-y', nargs=1, type=str, required=True)
    parser.add_argument('--diff', nargs=1, type=str, required=True)
    parser.add_argument('--highlight', nargs=1, type=str, required=True)
    parser.add_argument('--combined', nargs=1, type=str, required=True)
    parser.add_argument('--morphed', nargs=1, type=str, required=True)

    args = parser.parse_args()
    x_path:str = args.x[0]
    y_path:str = args.y[0]
    diff_path:str = args.diff[0]
    highlight_path:str = args.highlight[0]
    combined_path:str = args.combined[0]
    morphed_path:str = args.morphed[0]

    # print(x_path, y_path, diff_path, highlight_path, combined_path)

    (_, _, diff, thres_diff, morphed, combined) = compare(x_path, y_path)
    
    cv2.imwrite(morphed_path, morphed)
    cv2.imwrite(diff_path, diff)
    cv2.imwrite(highlight_path, thres_diff)
    cv2.imwrite(combined_path, combined)