import uuid
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os

def main():
    # Ask the user for the input file
    input_directory = input("Enter the path to the input directory: ")
       
    # List all the files in the input directory
    files = os.listdir(input_directory)

    # Choose a file from the input directory
    file_choice = input("Choose a file from the input directory: ")
    input_file = os.path.join(input_directory, file_choice)

    num_clips = int(input("How many clips do you want to create? "))

    # Ask the user for the output directory
    output_directory = input("Enter the output directory for the saved clips: ")

    # Generate the clips
    for i in range(num_clips):

        start_time = int(input("Enter the start time in seconds: "))
        end_time = int(input("Enter the end time in seconds: "))

        # Ask the user if they want to remove music
        remove_music_option = input("Remove music from the video clips? (y/n): ")
        remove_music = True if remove_music_option.lower() == "y" else False

        # Ask the user for the path to the music file
        music_file = input("Enter the path to the music file (leave blank to skip): ")

        # Generate a random output file name
        output_file = f"{output_directory}/{uuid.uuid4()}.mov"

        # Trim the video and resize it to the desired resolution
        ffmpeg_extract_subclip(input_file, start_time, end_time, targetname=output_file, height=1080, width=1920)

        # Remove music from the video clip if requested
        if remove_music:
            os.system(f"ffmpeg -i {output_file} -c copy -an {output_file}_nomusic.mov")

        # Remove metadata from the video clip
        os.system(f"ffmpeg -i {output_file} -map_metadata -1 -c copy -an {output_file}_nometa.mov")

if __name__ == "__main__":
    main()

    
