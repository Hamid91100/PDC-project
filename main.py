import parallel_filter

def main():
    input_image_path = "images/input_image.jpg"
    output_image_path = "images/output_image.jpg"
    num_processes = 4

    print("Before applying filter")

    parallel_filter.apply_parallel_filter(input_image_path, output_image_path, num_processes)

    print("Image filter applied successfully. Output saved to images folder")

if __name__ == "__main__":
    main()