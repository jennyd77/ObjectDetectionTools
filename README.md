# ObjectDetectionTools
Tools I have created to assist with creating datasets for object detection<br>

## create_lst.py<br>
&nbsp;&nbsp;&nbsp;Takes as input a labelled dataset exported in YOLO format.<br>
&nbsp;&nbsp;&nbsp;Output is 2 lst files - one for training and another for validation<br>

### Pre-requisites:<br>
&nbsp;&nbsp;&nbsp;python2.7<br>
   
### Usage:<br>
&nbsp;&nbsp;&nbsp;create_lst.py -i \<imagedir> -o \<outputfileprefix> -r \<ratio><br>
  
&nbsp;&nbsp;&nbsp;imagedir is the directory containing the YOLO output, it will have a data directory and a yolo-obj.cfg file<br>
&nbsp;&nbsp;&nbsp;outputfileprefix is the prefix that will be applied to the train.lst and val.lst files<br>
&nbsp;&nbsp;&nbsp;ratio determines the proportion of image records in each dataset, e.g. 0.9 will place 90% of images in training file<br>
  
### Output:<br>
&nbsp;&nbsp;&nbsp;\<prefix>_train.lst<br>
&nbsp;&nbsp;&nbsp;\<prefix>_val.lst<br>

## create_rec.py<br>
&nbsp;&nbsp;&nbsp;Takes as input a validation and training file in LST format and produces two corresponding .rec files<br>

### Pre-requisites:<br>
&nbsp;&nbsp;&nbsp;python2.7<br>
   
### Usage:<br>
&nbsp;&nbsp;&nbsp;create_rec.py -p \<prefix> -r \<root><br>
  
&nbsp;&nbsp;&nbsp;prefix is the same prefix supplied to create_lst.py<br>
&nbsp;&nbsp;&nbsp;root is the path to the lst files<br>
   
### Output:<br>
&nbsp;&nbsp;&nbsp;\<prefix\>_train.rec<br>
&nbsp;&nbsp;&nbsp;\<prefix\>_val.rec<br>
&nbsp;&nbsp;&nbsp;\<prefix>_train.idx<br>
&nbsp;&nbsp;&nbsp;\<prefix>_val.idx<br>
  
