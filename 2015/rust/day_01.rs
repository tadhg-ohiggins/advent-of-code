use std::fs;

const DAY: &str = "01";
const ANSWER1: usize = 74;
const ANSWER2: usize = 1795;

fn main() {
    let (input_file, test_file) = get_filenames();
    let input = fs::read_to_string(input_file).expect("error reading file");
    //let test_input = fs::read_to_string(test_file).expect("error reading file");

    //println!("{}, {}, {}, {}, {}", DAY, input_file, test_file, ANSWER1, ANSWER2);
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
    return data.matches("(").count() - data.matches(")").count();
}

fn convert_char_to_int(c: char) -> i32 {
    match c {
        '(' => 1,
        ')' => -1,
        _ => panic!("Not a parenthesis: x{}x", c),
    }
}

fn process_two(data: &str) -> usize {
    let mapped = data.trim().chars().map(convert_char_to_int);
    let mut rolling = 0;
    for (i, element) in mapped.enumerate() {
        rolling = rolling + element;
        if rolling == -1 {
            return i + 1;
        }
    }
    panic!("Never get to floor -1!")
}
