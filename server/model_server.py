import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import tensorflow as tf
import sys
import numpy as np

import inspect_model

ROOT_DIR = os.path.abspath("../")
sys.path.append(ROOT_DIR)  # To find local version of the library
sys.path.append(".")  # To find local version of the library


class ModelServer:
    def __init__(self, model_info_list):
        # self.sess = tf.InteractiveSession()

        #Load TF Config from tf-config file
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        #config.log_device_placement = True
        config.allow_soft_placement = True
        #config.gpu_options.per_process_gpu_memory_fraction = 0.4

        self.loaded_models = []
        for model_info in model_info_list:
            model_info_name = model_info['name']
            model_info_path = model_info['path']

            self.loaded_models[model_info.name].session = tf.Session(config=config)
            #TODO we need to check what tag to call. is it always 'serve'?
            self.loaded_models[model_info.name].loaded \
                = tf.saved_model.loader.load(self.loaded_models[model_info.name].session, ["serve"], model_info.path)
            self.loaded_models[model_info.name].graph = tf.get_default_graph()
            self.loaded_models[model_info.name].session.run(tf.global_variables_initializer())
            print('session for model info initialized: %s'%model_info)

            #TODO
            #inspect first model and get its input params and initial the tensor types
            #for each input tensor initialize the input param
            #for each output tensor initialize output param

            tag_set, method_name, input_params, output_params = inspect_model.inspect_models(model_info_path)

            print()
            print(model_info_path)
            print("----")
            print(tag_set)
            print(method_name)
            print(input_params)
            print(output_params)

            # see below code for examples
            # input params
            # for input_param in input_params:
                 self.loaded_models[model_info_name][input_param] = self.loaded_models[
                     model_info_name].graph.get_tensor_by_name(input_param)

            # output params
            # for output_param in output_params:
                 self.loaded_models[model_info_name][output_param] = self.loaded_models[
                     model_info_name].graph.get_tensor_by_name(output_param)

            # dict of output params
            # self.loaded_models[model_info_name].op_to_restore = (self.loaded_models[model_info_name].op_to_restore1, self.loaded_models[model_info_name].op_to_restore2)

            # self.loaded_models[model_info_name].output_dict = dictionary of output params

            '''
            #the below line is the way to do it
            self.loaded_models[model_info.name].input_params[input_param_name] 
            = self.loaded_models[model_info.name].graph.get_tensor_by_name(input_param_name)
            
            self.loaded_models[model_info.name].output_params[output_param_name] 
            = self.loaded_models[model_info.name].graph.get_tensor_by_name(output_param_name)
    
            self.loaded_models[model_info.name].output_dict = dictionary of output params
    
            OLD CODE FOR REFERENCE
            input params
            self.x_tensor_mrcnn_1 = self.graph_mrcnn.get_tensor_by_name("input_image:0")
            self.x_tensor_mrcnn_2 = self.graph_mrcnn.get_tensor_by_name("input_image_meta:0")
            self.x_tensor_mrcnn_3 = self.graph_mrcnn.get_tensor_by_name("input_anchors:0")
            
            output params
            self.op_to_restore1 = self.graph_mrcnn.get_tensor_by_name("mrcnn_detection/Reshape_1:0")
            self.op_to_restore2 = self.graph_mrcnn.get_tensor_by_name("mrcnn_mask/Reshape_1:0")
            
            dict of output params
            self.op_to_restore = (self.op_to_restore1, self.op_to_restore2)
            '''

        return

    def infer(self, model_name, input_values):
        #in a loop create a dictionary of inpout params and input values

        for input_val in input_values:
            x_test1 = input_val1
            x_test2 = input_val2
            x_test3 = input_val3
            feed_dict = {self.x_tensor_1: x_test1, self.x_tensor_2: x_test2,
                         self.x_tensor_3: x_test3}

            feed_dict.append(x_test1)

            opt = self.loaded_models[model_name].session.run(self.op_to_restore, feed_dict)

        for i in range(len(input_values)):
            x_test1 = input_values[i]
            x_test2 = input_val2
            x_test3 = input_val3
            feed_dict = {self.x_tensor_1: x_test1, self.x_tensor_2: x_test2,
                         self.x_tensor_3: x_test3}

            feed_dict.append(x_test1)

            opt = self.loaded_models[model_name].session.run(self.op_to_restore, feed_dict)

        return opt

    def infer_crop_classify(self, input_values):
        x_test = input_values.astype(np.float32)

        feed_dict = {self.x_tensor_crop_classify: x_test}
        opt = self.sess_bruise.run(self.op_to_restore_crop_classify, feed_dict)

        detections = opt

        return detections
