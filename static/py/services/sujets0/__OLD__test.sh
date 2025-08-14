set -e


# Check if an argument is provided to filter by question number
PATTERN=""
if [ "$1" != "" ]; then
    PATTERN="_$1_"
fi


# Process both question and correction files
for suffix in "question" "correction"; do
    # Adjust the file pattern based on whether a filter is provided
    if [ -z "$PATTERN" ]; then
        FILE_PATTERN="src/services/sujets0/spe_sujet1_*_$suffix.py"
    else
        FILE_PATTERN="src/services/sujets0/spe_sujet1*$PATTERN*$suffix.py"
    fi
    
    echo "Testing $suffix files..."
    for file in $FILE_PATTERN; do
        if [ -f "$file" ]; then
            echo "Running: $file"
            # Set PYTHONPATH for each command
            PYTHONPATH=".:$PYTHONPATH" python "$file"
            PYTHONPATH=".:$PYTHONPATH" python -m doctest "$file"
        fi
    done
done













# # Adjust the file pattern based on whether a filter is provided
# if [ -z "$PATTERN" ]; then
#     FILE_PATTERN="src/services/sujets0/spe_sujet1_*_question.py"
# else
#     FILE_PATTERN="src/services/sujets0/spe_sujet1*$PATTERN*question.py"
# fi

# for file in $FILE_PATTERN; do
#     if [ -f "$file" ]; then
#         # Set PYTHONPATH for each command
#         PYTHONPATH=".:$PYTHONPATH" python "$file"
#         PYTHONPATH=".:$PYTHONPATH" python -m doctest "$file"
#     fi
# done













# for file in src/services/sujets0/spe_sujet1_*_question.py; do
#     if [ -f "$file" ]; then
#         # Set PYTHONPATH for each command
#         PYTHONPATH=".:$PYTHONPATH" python "$file"
#     fi
# done
