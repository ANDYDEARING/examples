def create_histogram(file, band_number):
    """takes a file and a desired number of bands, prints
    the histogram, and returns nothing"""
    nums = get_nums_from_file(file)

    # if the band_number is invalid, exit the function
    if band_number < 2:
        print("Invalid number of bands")
        return None
    
    bands = get_bands(nums, band_number)
    print_histogram(bands)


def get_nums_from_file(file):
    """reads numbers from a passed file and returns a list
    of stripped strings converted to floats"""
    nums = []
    with open(file) as fh:
        for line in fh.readlines():
            nums.append(float(line.strip()))
    return nums


def get_bands(nums, band_number):
    """accepts a list of floats and a desired number of bands,
    returning a dictionary of bands and their frequencies. This
    function now uses the midpoint method, where the min and max
    values are at the midpoints of their respective ranges"""
    bands = {}
    min_num = min(nums)
    max_num = max(nums)
    
    # if the number of desired bands is not 1 or 0, find the band size
    # by dividing the range by the band_number - 1 because half
    # a range will be appended to the beginning and the end of the
    # dictionary by the midpoint method
    
    band_size = (max_num - min_num) / (band_number - 1)

    # make the histogram with ranges
    # initialize the bottom of the first range
    min_of_band = min_num - (band_size/2)
    for index in range(band_number):
        # compute the maximum of the range, make the key, and make the 
        # previous maximum the minimum for the next key. This corrects
        # the rounding error with some bands inherent in mixing addition
        # and division
        max_of_band = (index*band_size) + min_num + (band_size/2)
        bands[(min_of_band,max_of_band)] = 0
        min_of_band = max_of_band
    
    # add the numbers to the histogram
    for num in nums:
        if find_band(num, bands) is None:
            breakpoint()
        bands[find_band(num, bands)] += 1
        
    return bands

def find_band(num, ranges_dict):
    """accepts a dictionary with tuple keys of potential ranges and 
    returns the key where the num belongs, returning None if not 
    found"""

    for range_tuple in ranges_dict:
        if range_tuple[0] <= num < range_tuple[1]:
            # if the range is found, exit funcion
            correct_range_tuple = range_tuple
            return correct_range_tuple

    # if the range isn't found, return none
    return None

def print_histogram(bands):
    for band in sorted(bands.keys()):
        # limits decimal places to 1
        band_range = f"{round(band[0],1)}-{round(band[1],1)}"
        print(f"{band_range.rjust(15)} | {'*' * bands[band]}")


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description='Create a histogram')
    parser.add_argument('-b', '--band-number', default=10, type=int)
    parser.add_argument('file', help='file to read')
    args = parser.parse_args()

    file = Path(args.file)

    if file.is_file():
        create_histogram(file, args.band_number)
    else:
        print(f"{file} does not exist!")
        exit(1)
