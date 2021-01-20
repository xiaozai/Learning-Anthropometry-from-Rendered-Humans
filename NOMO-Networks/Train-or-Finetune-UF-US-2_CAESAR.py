from __future__ import print_function
import tensorflow as tf 
import RunHelpers_CAESAR as rh 
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--learning_rate",   default=1e-4, type=float, help='learning rate')
parser.add_argument("--lr_decay_step",   default=0,    type=int,   help='after each epoch, lr decreases')
parser.add_argument("--lr_decay_rate",   default=0.1,  type=float, help='new lr = lr * rate')
parser.add_argument("--batch_size",      default=32,   type=int,   help='batch size')
parser.add_argument("--nb_epoch",        default=30,   type=int,   help="num of trianing epochs")
parser.add_argument('--input_channels',  default=1,    type=int,   help='1 for silh, 3 for RGB')
parser.add_argument('--input_rows',      default=224,  type=int,   help="Image Height")
parser.add_argument('--input_cols',      default=124,  type=int,   help="Image Width")
parser.add_argument("--num_classes",     default=26,   type=int,   help="dimension of the labels")
parser.add_argument("--share_weights",   default=0,    type=int,   help="0 no share; 1 share weights")
parser.add_argument("--pre_model_path",  default='')
parser.add_argument('--output_path',     default='')
parser.add_argument("--train_files",     default='')

FLAGS = parser.parse_args()

#----------------------------------------------------------------------------------------------------
def print_args(args):
	print("------ Training Parameters ------------")
	print("--learning_rate   : %f" %args.learning_rate)
	print("--lr_decay_step   : %d" %args.lr_decay_step)
	print("--lr_decay_rate   : %f" %args.lr_decay_rate)
	print("--batch_size      : %d" %args.batch_size)
	print("--nb_epoch        : %d" %args.nb_epoch)
	print("--input_rows      : %d" %args.input_rows)
	print("--input_cols      : %d" %args.input_cols)
	print("--input_channels  : %d" %args.input_channels)
	print("--num_classes     : %d" %args.num_classes)
	print("--pre_model_path  : %s" %args.pre_model_path)
	print("--output_path     : %s" %args.output_path)
	print("---------------------------------------")

#----------------------------------------------------------------------------------------------------
def train_or_finetune(args):

	print_args(args)

	rh.train_or_finetune_UF_US_2(output_path    =args.output_path,
								 pre_model_path =args.pre_model_path,
							 	 train_files    =args.train_files,
							     share_weights  =args.share_weights,
							     batch_size     =args.batch_size, 
							     nb_epoch       =args.nb_epoch, 
						    	 learning_rate  =args.learning_rate, 
						    	 lr_decay_step  =args.lr_decay_step,
						    	 lr_decay_rate  =args.lr_decay_rate,
							     img_rows       =args.input_rows, 
							     img_cols       =args.input_cols, 
							     img_channels   =args.input_channels,
							     num_classes    =args.num_classes)

#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

	train_or_finetune(FLAGS)