#pragma once

#include <opencv2/opencv.h>    // Include OpenCV API

void downsample_min_4x4(const cv::Mat& source, cv::Mat* pDest);