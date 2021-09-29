use std::collections;
use std::fs;
use std::ops;

const DAY: &str = "03";
const ANSWER1: usize = 2565;
const ANSWER2: usize = 2639;

macro_rules! vadd {
    ( $( $x:expr ),* ) => {
        {
            let mut temp_vec = Vec::new();
            $(
                temp_vec.push($x);
            )*
            temp_vec.concat()
        }
    };
}

#[derive(Copy, Clone, Hash, Ord)]
struct Point {
    x: i32,
    y: i32,
}

impl ops::Add<Point> for Point {
    type Output = Point;

    fn add(self, _rhs: Point) -> Point {
        return Point {
            x: self.x + _rhs.x,
            y: self.y + _rhs.y,
        };
    }
}

impl ops::Sub<Point> for Point {
    type Output = Point;

    fn sub(self, _rhs: Point) -> Point {
        return Point {
            x: self.x - _rhs.x,
            y: self.y - _rhs.y,
        };
    }
}

impl ops::Mul<i32> for Point {
    type Output = Point;

    fn mul(self, _rhs: i32) -> Point {
        return Point {
            x: self.x * _rhs,
            y: self.y * _rhs,
        };
    }
}

impl PartialEq for Point {
    fn eq(&self, other: &Self) -> bool {
        self.x == other.x && self.y == other.y
    }
}
impl Eq for Point {}

fn move_point(coords: Point, direction: char) -> Point {
    let arrow = String::from(direction);
    let dir = match arrow.as_str() {
        "^" => Point { x: 1, y: 0 },
        "v" => Point { x: -1, y: 0 },
        ">" => Point { x: 0, y: 1 },
        "<" => Point { x: 0, y: -1 },
        _ => panic!("unknown direction"),
    };
    return coords + dir;
}

fn main() {
    let (input_file, test_file) = get_filenames();
    let mut input = fs::read_to_string(input_file).expect("error reading file");
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
    let visited: Vec<Point> = visit_points(Point { x: 0, y: 0 }, data.trim());
    let unique: collections::HashSet<Point> =
        visited.into_iter().collect::<collections::HashSet<Point>>();
    return unique.len();
}

fn process_two(data: &str) -> usize {
    let enumerated = data.trim().chars().into_iter().enumerate();
    let (even, odd): (Vec<(usize, char)>, Vec<(usize, char)>) =
        enumerated.partition(|&pair| pair.0 % 2 == 0);

    let santa_dirs: String = even.iter().map(|&pair| pair.1).collect::<String>();
    let robo_dirs: String = odd.iter().map(|&pair| pair.1).collect::<String>();
    let santa_points: Vec<Point> = visit_points(Point { x: 0, y: 0 }, santa_dirs.as_str());
    let robo_points: Vec<Point> = visit_points(Point { x: 0, y: 0 }, robo_dirs.as_str());

    let visited = vadd![santa_points, robo_points];
    // let visited = [santa_points, robo_points].concat();
    let unique: collections::HashSet<Point> =
        visited.into_iter().collect::<collections::HashSet<Point>>();
    return unique.len();
}

fn visit_point(mut visited: Vec<Point>, direction: char) -> Vec<Point> {
    let last: Point = visited.last().unwrap().clone();
    let moved: Point = move_point(last, direction);
    return vadd![visited, vec![moved]];
}

fn visit_points(origin: Point, directions: &str) -> Vec<Point> {
    return directions
        .chars()
        .into_iter()
        .fold(vec![origin], visit_point);
}
