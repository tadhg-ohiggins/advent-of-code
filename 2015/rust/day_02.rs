use std::fs;

const DAY: &str = "02";
const ANSWER1: usize = 1588178;
const ANSWER2: usize = 3783758;

fn main() {
    let (input_file, test_file) = get_filenames();
    let input = fs::read_to_string(input_file).expect("error reading file");
    //let test_input = fs::read_to_string(test_file).expect("error reading file");

    let x = process_one(&input);
    assert_eq!(x, ANSWER1);
    println!("{}", x);
    let y = process_two(&input);
    assert_eq!(y, ANSWER2);
    println!("{}", y);
}

fn get_filenames() -> (String, String) {
    let input: String = format!("../python/input-{day}.txt", day = DAY);
    let test: String = format!("../python/test-input-{day}.txt", day = DAY);
    return (input, test);
}

fn process_one(data: &str) -> usize {
    return data
        .trim()
        .split_terminator("\n")
        .map(parse_line)
        .map(get_surface_from_sides)
        .sum();
}

fn process_two(data: &str) -> usize {
    return data
        .trim()
        .split_terminator("\n")
        .map(parse_line)
        .map(get_ribbon_from_sides)
        .sum();
}

fn parse_line(line: &str) -> (usize, usize, usize) {
    let lwh = &line
        .split("x")
        .map(|chunk| chunk.parse().unwrap())
        .collect::<Vec<usize>>();
    return (lwh[0], lwh[1], lwh[2]);
}

fn get_surface_from_sides((length, width, height): (usize, usize, usize)) -> usize {
    let sides = vec![2 * length * width, 2 * width * height, 2 * height * length];
    let base: usize = sides.iter().sum();
    let small: usize = sides.iter().min().unwrap() / 2;
    return base + small;
}

fn get_ribbon_from_sides((length, width, height): (usize, usize, usize)) -> usize {
    let sides = vec![
        length + length + width + width,
        height + height + width + width,
        height + height + length + length,
    ];
    let small: usize = *sides.iter().min().unwrap();
    return small + (length * width * height);
}
