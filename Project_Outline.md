# <ins>**Project Outline**<ins>

## 1. Defining Supported Sports:
  - **American Football** (NCAA and NFL)
  - **Basketball** (NBA, NCAA)
  - **Soccer** (EPL, Champions League, MLS)
  - **Baseball** (MLB)
  - **Hockey** (NHL)
  - **Mixed Martial Arts** (MMA: specifically UFC)
## 2. Outcomes to Predict:
  - 1. **Match Winner**: Predict Winning Team/Individual of a game/match
  - 2. **Point Spread**: Predict how much a team win/loses by (regression)
  - 3. **Over/Under**: Predict if combined scores will go above or under the set betting line.
## 3. Feature Engineering
  ### Need features for neural network that applies to all sports but also caters to sport specific statistics
  **Universal Features**
  - **Team Stats**
    - Average of Points scored and allowed
    - Win/Loss record (recent data)
    - Efficiency (ex. yards per carry/pass in football, field goal percentage in basketball)
  - **Player Stats**
    - Top players performance
    - Injuries/Suspensions
  - **Game Context**
    - Home/away games
    - Back-to-back games/rest days
  - **Betting Data**
    - Moneyline Odds
    - Point Spreads and line movements
    - Implied probabilities from odds
  **Sport Specific Features**
    - **Basketball**: Player minutes, pace, three-point shooting
    - **Soccer**: Shots on goal, expected goals
    - **Baseball**: Pitcher Stats, betting averages
    - **MMA**: Reach, strikes landed, takedown accuracy
## 4. Data Strategy
  ### Handling multiple sports requires careful dataset structuring
  **Possible Data Sources**
    1. **APIs**:
      1. SportsRadar
      2. ESPN API
      3. SPortr API
      4. ODDs APi
    2. **Web Scraping**:
      1. Libraries (Beautiful Soup, Selenium) to scrape websites such as ESPN, NBA.com, or UFCStats.com
    3. **Public DataSets**:
      1. Kaggle
    4. **Data Pipeline**:
      1. **Collect**: Fetch data daily using APIs or scraping script
      2. **Transform**:
          1. Normalize and scale number values
          2. encode category variables(teams, players)
      3. **Store**:
          1. Structured Database (SQLLite, PostgreSQL) for ease of querying
          2. Separate datasets by sport but unify key fields (data, team names, odds)
## 5. Model Approach
### Flexible neural network that supports multiple sports needs modularity
**Architecture**
- **Shared Layers**:
  - Input Universal features through common network
- **Sports Specific Layers**
  - Separate sub-networks to process sport-specific features
- **Output Layer**:
  - Tailor output for each sport:
    - Classification for match winner
    - Regaression for point spreads
    - Binary classificaiton for over/under
**Example Architecture:**
Shared Layers:
Input → Dense → Dense (common features).
Split by Sport:
Dense → Output (e.g., basketball-specific subnetwork).
Dense → Output (e.g., soccer-specific subnetwork).
Merge Outputs:
Combined prediction for overall betting advice.
## 6. Challenges to Plan For
  1. **Imbalanced Data**:
     1. Upsets less common than expected outcomes. Oversample/weighted losses
  2. **Feature Consistency**:
     1. Not all features available for every sport, handle missing data correctly
  3. **Model Generalization**:
     1. Avoid overfitting to specific sport, use mix of shared and sports specific layers.
## 7. Action Plan
  1. Data Collection:
  -Start collecting data for 1-2 sports (e.g., NBA and NFL) to prototype the model.
  2. Feature Engineering:
  -Design universal and sport-specific features.
  3. Model Design:
  -Implement a simple shared layer + sport-specific layer architecture.
  4. Evaluation:
  -Validate predictions on each sport individually.
  -Simulate ROI for hypothetical bets.
