import tensorflow as tf
import numpy as np


def classify(fpath):

    image_data = tf.io.read_file(fpath)
    print(type(image_data),"image_data============")
    print(type(image_data),"image_data============")
    print(type(image_data),"image_data============")
    print(type(image_data),"image_data============")
    print(type(image_data),"image_data============")
    with tf.compat.v1.Session() as sess:
        # Run the session to evaluate the tensor
        numpy_array = sess.run(image_data)
    # Loads label file, strips off carriage return
    # label_lines = [line.rstrip() for line in tf.io.gfile.GFile("logs/output_labels.txt")]
    label_lines = [line.rstrip() for line in tf.io.gfile.GFile(r"C:\Users\Kareem\PycharmProjects\videosurveillance\logs\output_labels.txt")]
    print(label_lines, "label_lines")

    # Unpersists graph from file
    # with tf.io.gfile.GFile("logs/output_graph.pb", 'rb') as f:
    with tf.io.gfile.GFile(r"C:\Users\Kareem\PycharmProjects\videosurveillance\logs\output_graph.pb", 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.compat.v1.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': numpy_array})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        print(top_k,"top_k")
        print(top_k,"top_k")
        print(top_k,"top_k")
        print(top_k,"top_k")
        # idxx=top_k.index(2)
        print(label_lines[2])
        print(label_lines[2])
        print(label_lines[2])
        print(label_lines[2])
        print(label_lines[2])
        print("+++++++++++++++++++++++++")




        animal = label_lines[top_k[0]]
        print(animal, predictions[0][top_k[0]])
        return animal, predictions[0][top_k[0]]
