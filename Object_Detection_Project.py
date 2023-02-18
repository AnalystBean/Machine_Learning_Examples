import tensorflow as tf
import numpy as np
import os


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # suppress TensorFlow warnings
os.environ['PYTHONPATH'] = 'path/to/tensorflow/models/research:path/to/tensorflow/models/research/slim'


config_path = 'path/to/model/config'
model_dir = 'path/to/output/directory'


train_record_path = 'path/to/train.record'
val_record_path = 'path/to/val.record'

pipeline_config = tf.compat.v1.ConfigProto()
pipeline_config.gpu_options.allow_growth = True
pipeline_config.log_device_placement = False

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True

run_config = tf.estimator.RunConfig(model_dir=model_dir, session_config=pipeline_config, keep_checkpoint_max=3)

model_lib_v2.train_loop(
    run_config=run_config,
    model_fn=model_fn_builder(config),
    train_input_fn=train_input_fn,
    eval_input_fn=eval_input_fn,
    train_steps=num_steps,
    eval_steps=eval_steps,
    eval_on_train_data=False,
    use_tpu=False
)


inference_graph_path = 'path/to/inference/graph'
inference_graph = tf.Graph()

with inference_graph.as_default():
    od_graph_def = tf.GraphDef()

    with tf.gfile.GFile(inference_graph_path, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    with tf.Session(graph=inference_graph) as sess:
        # use the model for inference on new images
        image_path = 'path/to/test/image.jpg'
        image = np.array(Image.open(image_path))
        image_expanded = np.expand_dims(image, axis=0)
        image_tensor = inference_graph.get_tensor_by_name('image_tensor:0')
        boxes = inference_graph.get_tensor_by_name('detection_boxes:0')
        scores = inference_graph.get_tensor_by_name('detection_scores:0')
        classes = inference_graph.get_tensor_by_name('detection_classes:0')
        num_detections = inference_graph.get_tensor_by_name('num_detections:0')
        (boxes, scores, classes, num_detections) = sess.run(
            [boxes, scores, classes, num_detections],
            feed_dict={image_tensor: image_expanded})
        # display the results
        print('Boxes:', boxes)
        print('Scores:', scores)
        print('Classes:', classes)
        print('Num detections:', num_detections)