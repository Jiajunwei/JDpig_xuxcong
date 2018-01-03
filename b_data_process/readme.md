(1)运行image_process.py， 将上一步（yolo或tf_object_detection或手工截取）得到的图片通过padding的方法变为正方形，保证在之后的步骤中resize操作不会扭曲图片

(2)运行get_data_txt.py，对数据进行分割，并且将数据分割成50个储存文件，存在txt文件中（文件名 标签），方便之后大数据的分步读取

(3)运行create_h5_dataset.py, 将数据生成h5文件，这一步之后会得到50个储存训练集的.h5文件，以及50个储存验证集.h5文件

(4)create_tfrecord.py （可选）将数据变为另一种数据格式（tfrecord）