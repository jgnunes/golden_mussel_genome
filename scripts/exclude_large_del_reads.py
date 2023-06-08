import sys
import pysam

input_bam = sys.argv[1]
output_bam = input_bam.replace(".bam", ".filtered.bam")

# Open the input BAM file for reading
in_bam = pysam.AlignmentFile(input_bam, "rb")

# Open the output BAM file for writing
out_bam = pysam.AlignmentFile(output_bam, "wb", header=in_bam.header)

# Iterate over the reads in the input BAM file
for read in in_bam:

    # Check if the read has a deletion larger than 99 bp
    if any(op == 2 and length > 99 for op, length in read.cigartuples):
        continue  # Skip the read

    # Check if the read has clipping larger than 99 bp
    if any(op in (4, 5) and length > 99 for op, length in read.cigartuples):
        continue  # Skip the read

    else:
        # Write the read to the output BAM file
        out_bam.write(read)

# Close the BAM files
in_bam.close()
out_bam.close()
