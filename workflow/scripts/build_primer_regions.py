import pandas as pd


def parse_bed(log_file, out):
    print("chrom\tleft_start\tleft_end\tright_start\tright_end")
    for data_primers in pd.read_csv(
        snakemake.input[0],
        sep="\t",
        header=None,
        chunksize=chunksize,
        usecols=[0, 1, 2, 5],
    ):
        for row in data_primers.iterrows():
            row_id = row[0]
            row = row[1]
            if row[3] == "+":
                print(
                    "{chrom}\t{start}\t{end}\t\t".format(
                        chrom=row[0], start=row[1], end=row[2]
                    ),
                    file=out,
                )
            elif row[3] == "-":
                print(
                    "{chrom}\t\t\t{start}\t{end}".format(
                        chrom=row[0], start=row[1], end=row[2]
                    ),
                    file=out,
                )
            else:
                print("Invalid strand in row {}".format(row_id), file=log_file)


def parse_bedpe(log_file, out):
    for data_primers in pd.read_csv(
        snakemake.input[0],
        sep="\t",
        header=None,
        chunksize=chunksize,
        usecols=[0, 1, 2, 3, 4, 5],
    ):
        valid_primers = data_primers[0] == data_primers[3]
        valid_data = data_primers[valid_primers].copy()
        valid_data.iloc[:, [1, 4]] += 1
        print(
            valid_data.drop(columns=[3]).to_csv(
                sep="\t",
                index=False,
                header=["chrom", "left_start", "left_end", "right_start", "right_end"],
            ),
            file=out,
        )
        print(
            data_primers[~valid_primers].to_csv(sep="\t", index=False, header=False),
            file=log_file,
        )


chunksize = 10 ** 6
with open(snakemake.output[0], "w") as out:
    with open(snakemake.log[0], "w") as log_file:
        if snakemake.input[0].endswith("bedpe"):
            parse_bedpe(log_file)
        else:
            parse_bed(log_file)
