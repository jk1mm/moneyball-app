<h1 align="center">
 M⚾NEYBALL
</h1>

<p align="center">
 <strong> ~ Web analytics application that provides useful insights for your MLB team ~</strong>
</p>

<p align="center">
 <a href="https://share.streamlit.io/jk1mm/moneyball-app/main/app.py"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"></a>
 <a href="https://github.com/python"><img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt=":Language: Python"></a>
 <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
</p>

<p align="center">
<img src="docs/img/demo.gif" width=600>
</p>

<br>

⭐ All-in-one platform for extracting Major League Baseball's team insights. Moneyball provides quick access to 
[baseball-reference](https://www.baseball-reference.com/leagues/majors/) data and provides intuitive team rankings based 
on the following categories:
 - [Batting](https://github.com/jk1mm/moneyball-app#1-batting)
 - [Starting Pitching](https://github.com/jk1mm/moneyball-app#2-starting-pitching)
 - [Relief Pitching](https://github.com/jk1mm/moneyball-app#3-relief-pitching)
 - [Fielding](https://github.com/jk1mm/moneyball-app#4-fielding)

<br>

---

## Usage

### Navigating the Tool:
1. Select a `Season` and `Metric` of interest. This will initially generate some 
   [data](https://www.baseball-reference.com/leagues/majors/) of team statistics relevant to the selected values.
2. Choose a team in the `Select Team` dropdown to view the overall and category-based rankings. Details of the category
   scoring is explained in [Categorization Logic](https://github.com/jk1mm/moneyball-app#categorization-logic).

<br>

## Categorization Logic
Currently, there are 4 `Metric` available. Here is a breakdown of the category-based rankings available for each:

### 1. Batting
| Category | Description | Variables Involved
| --- | --- | --- |
| **Hitting** | Ability to get base hits | `BA`
| **Power** | Ability to hit for power  | `HR`
| **On Base** | Ability to get on base  | `OBP`
| **Base Stealing** | Ability to steal bases  | `SB` `CS`
| **Efficiency** | Ability to maximize run scoring opportunities  | `LOB` `R` `HR`
| ***OVERALL*** | Runs scored per game  | `R/G`


### 2. Starting Pitching
| Category | Description | Variables Involved
| --- | --- | --- |
| **Winning** | Ability to keep the game at a winning state | `Wgs` `Wlst` `Lsv`
| **Quality Start** | Ability to have quality starts  | `QS%`
| **Stamina** | Ability to accumulate large pitch counts | `80-99` `100-119` `≥120`
| **Efficiency** | Ability to accumulate innings | `IP/GS`
| ***OVERALL*** | Pitcher outing score | `GmScA`

### 3. Relief Pitching
| Category | Description | Variables Involved
| --- | --- | --- |
| **Saves** | Number of saves | `SV`
| **Holds** | Number of holds | `Hold`
| **Clean Closes** | Save rate | `SV%`
| **Win %**** | Ability to win as a result of relief | `Wgr` `Lgr`
| **Game Pressure** | Pressure faced by pitchers | `aLI`
| ***OVERALL***** | Ability to strand runners on base | `IS%`

### 4. Fielding 
| Category | Description | Variables Involved
| --- | --- | --- |
| **Defensive Efficiency** | Balls in play converted into outs | `DefEff`
| **DRS** | Relative number of defensive runs saved or cost | `Rdrs/yr`
| **Fld%** | Standard fielding percentage | `Fld%`
| **Good Plays** | Good Plays/Misplays runs above average | `Rgood`
| **DP** | Number of double plays completed | `DP`
| ***OVERALL***** | [Total Zone Runs](https://www.baseball-reference.com/about/total_zone.shtml): Considering outfield arms, infield double play induces, catcher efficiency | `Rtot/yr`

- Metrics in ** needs to be re-evaluated for more proper evaluation.

<br>

## Setup

### Common Issues
#### SSL Certs
On Mac, go to `Applications/python3._` and double click `Install Certificates`
