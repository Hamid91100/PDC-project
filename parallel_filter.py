from PIL import Image, ImageFilter
import multiprocessing

def apply_filter(image_chunk, filter_name):
    # Apply the specified filter to the image chunk
    
    if filter_name == 'black_and_white':
        return image_chunk.convert("L")  
    
    # Convert to black and white
    elif filter_name == 'blur':
        return image_chunk.filter(ImageFilter.BLUR)
    
    # Convert to bluish contrast
    elif filter_name == 'blue':
        return apply_blue_filter(image_chunk)

        # Convert to Sharpen    
    elif filter_name == 'sharpen':
        return image_chunk.filter(ImageFilter.SHARPEN)
    
    else:
        return image_chunk  
    # No filter

def apply_blue_filter(image_chunk):
    # Apply a blue filter by extracting and enhancing the blue channel
    r, g, b = image_chunk.split()
    
    enhanced_blue = b.point(lambda i: i * 1.5)
    return Image.merge('RGB', (r, g, enhanced_blue))

def apply_parallel_filter(input_path, base_output_path, num_processes):
    # Open the input image
    input_image = Image.open(input_path)
    
    width, height = input_image.size

    # Divide the image into chunks for parallel processing
    chunk_size = height // num_processes
    chunks = [(0, i * chunk_size, width, (i + 1) * chunk_size) for i in range(num_processes)]

    # List of filters to apply in parallel
    filters_to_apply = ['black_and_white', 'blur', 'blue', 'sharpen']

    for filter_name in filters_to_apply:
        # Use multiprocessing to apply filters in parallel
        with multiprocessing.Pool(processes=num_processes) as pool:
            result_chunks = pool.starmap(apply_filter, [(input_image.crop(chunk), filter_name) for chunk in chunks])

        # Create a new image to paste the filtered chunks
        output_image = Image.new("RGB", (width, height))

        # Paste the filtered chunks into the output image
        for i, chunk in enumerate(result_chunks):
            output_image.paste(chunk, (0, i * chunk_size))

        # Save the output image with a distinct filename based on the filter
        output_filename = f"{base_output_path}_{filter_name}.jpg"
        output_image.save(output_filename)

        # Print a success message
        print(f"Image filter '{filter_name}' applied successfully. Output saved to {output_filename}")

if __name__ == "__main__":
    # Call the apply_parallel_filter function with the specified parameters
    apply_parallel_filter("images/input_image.jpg", "images/output_image", num_processes=4)