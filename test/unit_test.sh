#!/bin/bash

# Execute the archive script using all option permutations.
odir='archives'

script=../archive_file.py
fbase=example_

# Clean up old test data first.
rm -rf ${odir} ${fbase}

# Run through the permutations.
i=1
for da_opt in ' ' '--da='${odir} # archive directory option
do

    for v_opt in ' ' '-v' # verbose flag
    do

        for z_opt in ' ' '-z' # gzip flag
        do
            # Make a file to archive.
            example_file=${fbase}${i}.txt
            echo "Archive file unit test file contents" > ${example_file}
            echo "--> Example Unit Test Permutation "${i} >> ${example_file}
            echo >> ${example_file}
            cat ${script} >> ${example_file}

            cmdo="${script} ${example_file} ${da_opt} ${v_opt} ${z_opt}"

            for dr_opt in '--dry-run' ' ' # dry-run flag
            do

                cmd="${cmdo} "${dr_opt}

                echo
                echo
                echo
                echo '######################################################'
                echo '## Executing Unit Test Permutation '${i}
                echo
                echo ${cmd}

                ${cmd}

                echo
                echo '##'
                echo '######################################################'

            done
            i=$((${i} + 1))
        done
    done
done
