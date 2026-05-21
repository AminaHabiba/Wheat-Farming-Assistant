# src/preprocessing/augmentation.py

import numpy as np
from keras.preprocessing.image import ImageDataGenerator


def get_train_datagen():
    """
    ImageDataGenerator for training with augmentation.
    Simulates real-world variations farmers face:
    - rotation     : any photo angle
    - flip         : disease on both leaf sides
    - zoom         : different camera distances
    - brightness   : different field lighting
    - shift        : leaf not always centered

    Output : ImageDataGenerator object
    """
    return ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        zoom_range=0.15,
        brightness_range=[0.8, 1.2],
        fill_mode="nearest"
    )


def get_val_test_datagen():
    """
    ImageDataGenerator for val and test.
    Only normalization — no augmentation.
    Keeps evaluation honest and consistent.

    Output : ImageDataGenerator object
    """
    return ImageDataGenerator(rescale=1.0 / 255)


def get_data_generators(processed_path, classes,
                        img_size=(224, 224),
                        batch_size=32):
    """
    Creates all three generators at once.

    processed_path : Path to dataset/processed/
    classes        : list of class names
    img_size       : target size (default 224x224)
    batch_size     : images per batch (default 32)

    Output : tuple (train_gen, val_gen, test_gen)
    """
    train_dg      = get_train_datagen()
    val_test_dg   = get_val_test_datagen()

    train_gen = train_dg.flow_from_directory(
        str(processed_path / "train"),
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        classes=classes,
        shuffle=True,
        seed=42
    )
    val_gen = val_test_dg.flow_from_directory(
        str(processed_path / "val"),
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        classes=classes,
        shuffle=False
    )
    test_gen = val_test_dg.flow_from_directory(
        str(processed_path / "test"),
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        classes=classes,
        shuffle=False
    )
    return train_gen, val_gen, test_gen


def augment_single_image(img_array, n_samples=5):
    """
    Generates n augmented versions of one image.
    Useful for visualizing augmentation effects.

    img_array : numpy array (H, W, 3) normalized
    n_samples : number of versions to generate

    Output : list of numpy arrays (H, W, 3)
    """
    datagen          = get_train_datagen()
    augmented_images = []
    img_batch        = img_array.reshape(
                           (1,) + img_array.shape)

    for batch in datagen.flow(img_batch,
                               batch_size=1, seed=42):
        augmented_images.append(batch[0])
        if len(augmented_images) >= n_samples:
            break
    return augmented_images


if __name__ == "__main__":
    train_dg = get_train_datagen()
    val_dg   = get_val_test_datagen()
    print("Train DataGenerator:")
    print(f"  rescale        : {train_dg.rescale}")
    print(f"  rotation_range : {train_dg.rotation_range}")
    print(f"  horizontal_flip: {train_dg.horizontal_flip}")
    print(f"  zoom_range     : {train_dg.zoom_range}")
    print()
    print("Val/Test DataGenerator:")
    print(f"  rescale        : {val_dg.rescale}")
    print(f"  augmentation   : None")

    dummy = np.random.randint(
                0, 255, (224, 224, 3),
                dtype=np.uint8
            ).astype(np.float32) / 255.0
    samples = augment_single_image(dummy, n_samples=3)
    print(f"\nAugmented samples : {len(samples)} ✅")
    print("augmentation.py working correctly!")