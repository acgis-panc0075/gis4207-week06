set base=..\..\..\..\data\BatchClipDataMarking
python batch_clipper.py
python batch_clipper.py ..\not_enough_args
python batch_clipper.py %base%\TargetData %base%\Sites %base%\Output 