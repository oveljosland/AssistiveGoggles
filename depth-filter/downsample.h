#pragma once

#include <opencv4/opencv2/opencv.hpp>    // Include OpenCV API

void downsample_min_4x4(const cv::Mat& source, cv::Mat* pDest);