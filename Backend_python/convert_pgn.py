# To get the data from the pgn file and convert it into a csv file wth columns 
# Player_White [Name] , Player_Black , Time_Control(Classical , Rapid , Blitz , Bullet) , Who_won(B or W) , Date , Game [1. Nf3  d5 2. e3  Nf6 3 ...]


# example of a pgn 
example = """
[Event "2019-world-rapid-championship"]
[White "Firouzja, Alireza"]
[Black "Giri, Anish"]
[WhiteFideId "12573981"]
[BlackFideId "24116068"]
[Result "1/2-1/2"]
[Round "07"]
[Date "Fri Dec 27 2019"]
[WhiteClock "0:04:25"]
[BlackClock "0:05:16"]


1. Nf3  d5 2. e3  Nf6 3. c4  c6 4. Nc3  e6 5. b3  Bd6 6. Bb2  O-O 7. Be2  b6 8. Rc1  Bb7 9. cxd5  exd5 10. O-O  Re8 11. Qc2  Nbd7 12. Qb1  Rc8 13. Rfd1  Ne5 14. d4  Nxf3+ 15. Bxf3  Rc7 16. Ne2  Ne4 17. Ng3  Bxg3 18. hxg3  Bc8 19. Qc2  Bf5 20. Qe2  Qd6 21. a3  a5 22. Qa6  Rb8 23. b4  axb4 24. axb4  b5 25. Bxe4  Bxe4 26. Bc3  h5 27. Be1  Bf5 28. Rc5  Qd7 29. Rdc1  Rbc8 30. Qa3  Ra7 31. Qc3  Ra6 32. f3  Rca8 33. Rxc6  Rxc6 34. Qxc6  Qxc6 35. Rxc6  Ra1 36. Kf2  Ra2+ 37. Kg1  Ra1 1/2-1/2


[Event "2019-world-blitz-championship"]
[White "Giri, Anish"]
[Black "Firouzja, Alireza"]
[WhiteFideId "24116068"]
[BlackFideId "12573981"]
[Result "0-1"]
[Round "18"]
[Date "Mon Dec 30 2019"]
[WhiteClock "0:00:01"]
[BlackClock "0:00:12"]


1. Nf3  Nf6 2. c4  g6 3. Nc3  Bg7 4. e4  d6 5. d4  O-O 6. Be2  e5 7. O-O  Nc6 8. dxe5  Nxe5 9. Nxe5  dxe5 10. Be3  Be6 11. Qc2  c6 12. b4  Re8 13. Rfd1  Qc8 14. h3  h5 15. Rab1  Kh7 16. a4  Bh6 17. Bxh6  Kxh6 18. Qc1+  Kg7 19. a5  Qc7 20. Qe3  b6 21. a6  Rad8 22. c5  b5 23. Rd6  Rxd6 24. cxd6  Qb6 25. Qxb6  axb6 26. Bxb5  cxb5 27. Nxb5  Ra8 28. Nc7  Ra7 29. f3  Bd7 30. Rc1  Kf8 31. b5  Ng8 32. Kf2  f6 33. h4  Nh6 34. Nd5  Nf7 35. Nxb6  Bxb5 36. Rc8+  Kg7 37. Rc5  Bxa6 38. d7  Rb7 39. Rc6  Bb5 40. Rd6  Rb8 41. Rd5  Rxb6 0-1

"""

import csv

def parse(filename):

    # Read the file content
    with open(filename, 'r') as file:
        data = file.read()

    # Split the data into separate games

    games = data.strip().split("\n\n\n")

    formated_games = []

    for i in range(len(games)-1):
        formated_games.append(games[i] + "\n" + games[i+1])

    return formated_games

def get_time_control(time_string):
    
    try:
        if ':' in time_string:
            segments = time_string.split(':')
            main_time_part = segments[0]
            extra_time_part = segments[1] if len(segments) > 1 else None

        
            if '/' in main_time_part:
                moves, main_time = main_time_part.split('/')
            
            if '+' in main_time:
                main_time = int(main_time.split('+')[0])
            else:
                main_time = int(main_time)

            if '+' in extra_time_part:
                extra_time = int(extra_time_part.split('+')[1])
            else:
                extra_time = 0
            
            if main_time == "60":
                return "Bullet"

            main_time /= 60  # convert to minutes
        else:

            if time_string == "60":
                return "Bullet"

            main_time, extra_time = map(int, time_string.split('+'))
            main_time /= 60  # convert to minutes
        

        if main_time <= 5:
            return "Blitz"
        elif 5 < main_time <= 30:
            return "Rapid"
        elif main_time > 30:
            return "Classical"
        else:
            return "Unknown"
    except Exception as e:
        return "Unknown"
    

def convert_pgn_to_csv(filename):

    parsed_data = {}
    all_games = parse(filename)
    for i, game in enumerate(all_games):
        lines = game.split('\n')
        game_info = {}
        game_moves = []

        for line in lines:
            if line.startswith('['):
                key, value = line[1:-1].split(' ', 1)
                game_info[key] = value.strip('"')
            elif line:
                game_moves.append(line.strip())

        # Determine time control
        event_name = game_info.get("Event", "").lower()


        TimeControl = game_info.get("TimeControl", "")
        if TimeControl == "":
            if "rapid" in event_name:
                time_control = "Rapid"
            elif "blitz" in event_name:
                time_control = "Blitz"
            elif "classical" in event_name:
                time_control = "Classical"
            elif "bullet" in event_name:
                time_control = "Bullet"
            else:
                time_control = "Unknown"
        else:
            time_control = get_time_control(TimeControl)
        print (TimeControl,time_control)
        
        # Determine winner
        result = game_info.get("Result", "")
        if result == "1-0":
            who_won = "W"
        elif result == "0-1":
            who_won = "B"
        else:
            who_won = "Draw"
        

        # Collect the necessary data
        parsed_data["Game No: " + str(i+1)] = {
            "Game_Number": str(i+1),
            "Player_White": game_info.get("White", ""),
            "Player_Black": game_info.get("Black", ""),
            "Time_Control": time_control,
            "Who_won": who_won,
            "Date": game_info.get("Date", ""),
            "Game": ' '.join(game_moves)
        }

    # Write to CSV
    csv_file = "Nodirbek_vs_Magnus.csv"
    csv_columns = ["Game_Number", "Player_White", "Player_Black", "Time_Control", "Who_won", "Date", "Game"]

    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for game in parsed_data.values():
            writer.writerow(game)

    print(f"Data written to {csv_file}")

    return parsed_data


convert_pgn_to_csv("/Users/devansh/Desktop/Project/prediction_model/Games_dataset/Nodirbek_vs_other/Nodirbek vs Magnus.pgn")


