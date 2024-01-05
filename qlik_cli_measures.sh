#!/bin/bash

# Qlik CLI command to list apps
qlik_command="qlik app measure ls --app 'Test App'"

# Run the Qlik CLI command and capture the output
output=$(eval $qlik_command)

# # Print the list of apps
# echo "List of Qlik Apps:"
# echo "$output"
csv_file="measure_list.csv"
#!/bin/bash
# Use a for loop to extract and display the measure names
IFS=$'\n' # Set the Internal Field Separator to newline

# Loop through each line of the output
for line in $output; do
    # Check if the line contains "Measure Name:" to extract measure names
    if [[ $line == *"TTC"* ]]; then
        # Extract and display the measure name
        measure_name="${line##*Measure Name: }"
        echo "Measure Name: $measure_name"
        echo "$measure_name" >> "$csv_file"
    fi
done

echo "Results saved to $csv_file"