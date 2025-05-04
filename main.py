import sys
import csv
import os

def split_csv(file_path: str, lines_per_file: int, output_dir: str) -> None:
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # 出力フォルダが存在しない場合は作成
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.reader(csvfile))
        header = reader[0]
        rows = reader[1:]
        
        total_parts = (len(rows) + lines_per_file - 1) // lines_per_file
        if total_parts == 1:
            print("警告! 1つのファイルしか生成されません!")

        for i in range(total_parts):
            part_rows = rows[i * lines_per_file : (i + 1) * lines_per_file]
            output_path = os.path.join(output_dir, f"{base_name}_part{i+1}.csv")
            with open(output_path, 'w', newline='', encoding='utf-8') as out_csv:
                writer = csv.writer(out_csv)
                writer.writerow(header)
                writer.writerows(part_rows)
            print(f"書き出しました: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("使い方: csv_cutter_py.exe <csvのパス> <1ファイルごとの行数> <出力フォルダ>")
        sys.exit(1)

    csv_path = sys.argv[1]
    try:
        lines_per_file = int(sys.argv[2])
    except ValueError:
        print("行数は整数で指定してください")
        sys.exit(1)

    output_dir = sys.argv[3]
    if not os.path.isfile(csv_path):
        print("指定されたCSVファイルが見つかりません")
        sys.exit(1)

    if not os.path.exists(output_dir):
        print(f"保存先フォルダが存在しないため作成します: {output_dir}")
        os.makedirs(output_dir)
    else:
        print(f"保存先フォルダは既に存在します: {output_dir}")

    split_csv(csv_path, lines_per_file, output_dir)
