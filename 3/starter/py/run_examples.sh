# shell script to test all examples

# # test on all files
# for file in $(find ../examples -name "*.bx"); do
#     echo $file 
#     python3 bxcc.py $file
#     echo -e '\n'
# done

# run all executables
# for file in $(find ../examples -name "*.exe"); do
#     echo $file 
#     $file
#     echo -e '\n'
# done

# test all error files
for file in $(find ../regression -name "*.bx"); do
    echo $file 
    python3 bxcc.py $file
done
