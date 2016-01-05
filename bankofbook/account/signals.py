from django.dispatch import Signal

avatar_crop_done = Signal(providing_args=['user_id', 'avatar_original', 'avatar_name', 'avatar_cropped_coordinate','isCurrent'])