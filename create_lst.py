#!/usr/local/bin/python
# This script takes as input an object detection dataset prepared in YOLO format
# In order to ceate the YOLO formatted dataset, I used the opensource tool VoTT:
#    https://github.com/Microsoft/VoTT
# All information for how to format the LST file was taken from the following site:
#    https://gluon-cv.mxnet.io/build/examples_datasets/detection_custom.html
# For information on the format of YOLO I used the following site:
#    https://github.com/AlexeyAB/Yolo_mark/issues/60
# This script is written for Python 2.7 but it really should be updated for Python 3 (because it's 2018 after all)

import sys, getopt
import os, glob
import cv2
import random
from random import choice


def main(argv):
   try:
      opts, args = getopt.getopt(argv,"hi:o:r:",["idir=","ofilepre=","ratio="])
   except getopt.GetoptError:
      print 'create_lst.py -i <imagedir> -o <outputfileprefix> -r <ratio>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'create_lst.py -i <imagedir> -o <outputfileprefix> -r <ratio>'
         sys.exit()
      elif opt in ("-i", "--idir"):
         img_dir = arg
      elif opt in ("-o", "--ofilepre"):
         outputfileprefix = arg
      elif opt in ("-r", "--ratio"):
         ratio = arg

   # Create an indexed list of all image files in RAM
   r_ordered_list = []
   index=0
   img_dir_path = img_dir + "/data/obj"
   for file in glob.glob(img_dir_path + "/*.jpg"): 
      r_ordered_list.append(str(index) + " " + file)
      index += 1

   # Randomly organise the list of all image files
   r_shuffled_list = random.sample(r_ordered_list, len(r_ordered_list))
   del r_ordered_list  # Do the right thing and free the memory

   # Create separate lists for training data and validation data. Split using provided ratio
   max=int(round(len(r_shuffled_list)*float(ratio)))
   r_train_list = r_shuffled_list[0:max]
   r_val_list = r_shuffled_list[max:]
   del r_shuffled_list # Free up memory

   # Read the YOLO output located in imagedir
   # For each image listed in train.txt and val.txt
   # Determine the dimensions of the image (height,width)
   # Read the txt file for the image and determine the bounding boxes
   # Write LST file in tab delimited format: index 4 5 0.0 xmin ymin xmax ymax ... img_file

   fname_train_lst = outputfileprefix + "_train.lst"
   fname_val_lst = outputfileprefix + "_val.lst"
   print "Writing training LST data to " + fname_train_lst
   print "Writing validation LST data to " + fname_val_lst
   create_lst_file(fname_train_lst,r_train_list)
   create_lst_file(fname_val_lst,r_val_list)

def create_lst_file(fname_lst,list):
   f_file_lst = open(fname_lst, "w")  # f_file_lst will need to be closed later, this is the file we will write to
   for entry in list:
      index, img_file = entry.split(" ")
      img=cv2.imread(img_file)
      height, width = img.shape[:2]
      # Create start of entry for this image - index<tab>header
      #   where header consists of 4 items: num_header_items(4 in this case)<tab>max_len_label(we will use 5)<tab>img_width<tab>img_height
      lst_entry = str(index) + "\t4\t5\t" + str(width) + "\t" + str(height)
      individual_image_txt_file=os.path.splitext(img_file)[0] + '.txt'
      with open(individual_image_txt_file) as f_ind_txt_file: #f_ind_txt_file will auto-close, this is the text file containing BB information for an individual image
         for object_bb in f_ind_txt_file: # Each individual txt file will contain one or more bounding box objects. We must parse each one.
            if object_bb[-1:] == "\n":
               object_bb = object_bb[:-1]
            obj_class, xmid, ymid, bb_width, bb_height = object_bb.split(" ") # Split each BB information line into its components
            # Convert BB details to format required by LST
            xmin = float(xmid) - (float(bb_width) / 2)
            ymin = float(ymid) - (float(bb_height) / 2)
            xmax = float(xmid) + (float(bb_width) / 2)
            ymax = float(ymid) + (float(bb_height) / 2)
            lst_entry = lst_entry + "\t" + obj_class + ".0\t" + str(xmin) + "\t" + str(ymin) + "\t" + str(xmax) + "\t" + str(ymax) # Append current BB object to lst_entry
      lst_entry = lst_entry + "\t" + img_file
      f_file_lst.write(lst_entry + '\n')
   f_file_lst.close() # We have finished writing to this LST file. Close it now

if __name__ == "__main__":
   main(sys.argv[1:])



