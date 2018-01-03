(1)为了排除背景数据对模型的影响，我们使用yolo-9000算法提取出视频中每一帧的猪，代码来源于https://github.com/philipperemy/yolo-9000. 我们对其代码做了修改，将yolo解压包的代码解压后覆盖 darknet/src下同名文件即可

(2)经观察后发现，虽然yolo-9000对猪的识别不一定会归于hog类，但是基本上所有的框都会以视频中的猪为主体，因此在取框的时候，我们不以hog类的框为输出图像，而是以置信度为参考标准。

(3)我们保留所有置信度大于0.1的窗口

(4)每个视频大约能得到一万多张ROI图片，我们按大小排序，选取大约前4000张图片，并剔除不相关的物体图片以及背景干扰较大的图片（比如没有框到猪身上，或者只框了极小部分的猪），将其作为训练集和验证集。

(5)最后得到94677张图片


darknet的用法：
./darknet detector demo cfg/combine9k.data cfg/yolo9000.cfg ../yolo9000-weights/yolo9000.weights  -prefix output <path_to_your_video_mp4> -thresh 0.15
./darknet detector demo cfg/combine9k.data cfg/yolo9000.cfg ../yolo9000-weights/yolo9000.weights  1.mp4