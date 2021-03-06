#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/3 0003 下午 8:20
# @Author  : Lovin
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/2 0002 下午 1:38
# @Author  : Lovin
#coding=utf-8
#tensorflow高效数据读取训练
import tensorflow as tf
import cv2
import os

#制作train.txt文件格式，每一行：图片路径名类别标签
def file_to_txt():
    path = 'G:/re/train/'
    folder_list = os.listdir(path)
    with open('train.txt','wt') as f:
        for folder in folder_list:
            img_list = os.listdir(path + folder)
            for image in img_list:
                f.write(folder + '/' +image + ' ' + folder + '\n')




#将数据打包，转换成tfrecords格式，以便后续高效读取
def encode_to_tfrecords(data_lable_file, data_root, new_name='data.tfrecords', resize=None):
    # writer = tf.python_io.TFRecordWriter(data_root + '/' + new_name)
    writer = tf.python_io.TFRecordWriter(new_name)
    num_example = 0
    with open(data_lable_file, 'r') as f:
        for data_lable in f.readlines():
            data_lable = data_lable.split()
            # print(data_lable)
            image = cv2.imread(data_root + "/" + data_lable[0])
            if resize is not None:
                image = cv2.resize(image, resize)
            height, width, nchannel = image.shape
            label = int(data_lable[1])
            # print(
            #     tf.train.Feature(int64_list=tf.train.Int64List(value=[height])),tf.train.Feature(int64_list=tf.train.Int64List(value=[label]))
            # )
            example = tf.train.Example(features=tf.train.Features(feature={
                'height': tf.train.Feature(int64_list=tf.train.Int64List(value=[height])),
                'width': tf.train.Feature(int64_list=tf.train.Int64List(value=[width])),
                'nchannel': tf.train.Feature(int64_list=tf.train.Int64List(value=[nchannel])),
                'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image.tobytes()])),
                'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label]))
            }))
            serialized = example.SerializeToString()
            writer.write(serialized)
            num_example += 1
    print(data_lable_file, "样本数据量：", num_example)
    writer.close()


#读取tfrecords文件
def decode_from_tfrecords(filename,num_epoch=None):
    # filename_queue=tf.train.string_input_producer([filename],num_epochs=num_epoch)#因为有的训练数据过于庞大，被分成了很多个文件，所以第一个参数就是文件列表名参数
    filename_queue = tf.train.string_input_producer([filename])
    reader=tf.TFRecordReader()
    _,serialized=reader.read(filename_queue)
    example=tf.parse_single_example(serialized,features={
        'height':tf.FixedLenFeature([],tf.int64),
        'width':tf.FixedLenFeature([],tf.int64),
        'nchannel':tf.FixedLenFeature([],tf.int64),
        'image':tf.FixedLenFeature([],tf.string),
        'label':tf.FixedLenFeature([],tf.int64)
    })
    image=tf.decode_raw(example['image'],tf.uint8)
    image=tf.reshape(image,tf.stack([
        tf.cast(example['height'], tf.int32),
        tf.cast(example['width'], tf.int32),
        tf.cast(example['nchannel'], tf.int32)]))

    # image = tf.reshape(image, [128, 128, 3])
    # image = tf.cast(image, tf.float32) * (1. / 255) - 0.5

    label = tf.cast(example['label'], tf.int32)
    return image,label
#根据队列流数据格式，解压出一张图片后，输入一张图片，对其做预处理、及样本随机扩充
def get_batch(image, label, batch_size,crop_size):
        #数据扩充变换
    distorted_image = tf.random_crop(image, [crop_size, crop_size, 3])#随机裁剪
    distorted_image = tf.image.random_flip_up_down(distorted_image)#上下随机翻转
    #distorted_image = tf.image.random_brightness(distorted_image,max_delta=63)#亮度变化
    #distorted_image = tf.image.random_contrast(distorted_image,lower=0.2, upper=1.8)#对比度变化

    #生成batch
    #shuffle_batch的参数：capacity用于定义shuttle的范围，如果是对整个训练数据集，获取batch，那么capacity就应该够大
    #保证数据打的足够乱
    images, label_batch = tf.train.shuffle_batch([distorted_image, label],batch_size=batch_size,
                                                 num_threads=16,capacity=50000,min_after_dequeue=10000)
    #images, label_batch=tf.train.batch([distorted_image, label],batch_size=batch_size)



    # 调试显示
    #tf.image_summary('images', images)
    return images, tf.reshape(label_batch, [batch_size])
#这个是用于测试阶段，使用的get_batch函数
def get_test_batch(image, label, batch_size,crop_size):
    #数据扩充变换
    distorted_image=tf.image.central_crop(image,39./45.)
    distorted_image = tf.random_crop(distorted_image, [crop_size, crop_size, 3])#随机裁剪
    images, label_batch=tf.train.batch([distorted_image, label],batch_size=batch_size)
    return images, tf.reshape(label_batch, [batch_size])
#测试上面的压缩、解压代码
def test():
    encode_to_tfrecords("data/train.txt","data",(128,128))
    image,label=decode_from_tfrecords('data/data.tfrecords')
    batch_image,batch_label=get_batch(image,label,3)#batch 生成测试
    init=tf.initialize_all_variables()
    with tf.Session() as session:
        session.run(init)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        for l in range(100000):#每run一次，就会指向下一个样本，一直循环
            #image_np,label_np=session.run([image,label])#每调用run一次，那么
            '''cv2.imshow("temp",image_np)
            cv2.waitKey()'''
            #print label_np
            #print image_np.shape


            batch_image_np,batch_label_np=session.run([batch_image,batch_label])
            print(batch_image_np.shape)
            print(batch_label_np.shape)



        coord.request_stop()#queue需要关闭，否则报错
        coord.join(threads)
#test()
if __name__ == '__main__':
    # file_to_txt()
    # encode_to_tfrecords(data_lable_file="train.txt", data_root="G:/re/train", resize=(128, 128))
    image, label = decode_from_tfrecords(filename='data.tfrecords')
    print(image)
    print(label)
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        print(sess.run(label))
        # coord = tf.train.Coordinator()
        # threads = tf.train.start_queue_runners(coord=coord)
        # for l in range(100):


    # batch_image, batch_label = get_batch(image, label, 3)
    # print(batch_image,batch_label)
