
host = "localhost"
port = 60059
data_size = 1024*1024
header_size = 100

model_conf_path = "models.conf"
tf_conf_path = "tf.conf"


'''
models.conf:
{
    {
        model.name:''
        model.path:''
    },
    {
        model.name:''
        model.path:''
    }
}

models:
  model-1:
    input:
      input_param_1:input_value_1
      input_param_2:input_value_2
      input_param_3:input_value_3
    output:
      output_param_1:output_value_1
      output_param_2:output_value_2
      output_param_3:output_value_3
  model-2:
    input:
      input_param_1:input_value_1
      input_param_2:input_value_2
    output:
      output_param_1:output_value_1
'''