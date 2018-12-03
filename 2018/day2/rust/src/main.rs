use std::collections::HashMap;

let SYMOLS = ['a', 'b', 'c', 'd', 'e', 'f'];

fn foo(s: &str) -> (u8, u8) {
    let mut map = HashMap<char, u8>;
    for key in SYMOLS { map.insert(key, 0)}
    for i in [0..s.len()] {
        let ch = s[i];
        for key in SYMBOLS {
            if ch == key {
                println!("yep");
            }




fn main() {
    println!("Hello, world!");
}
