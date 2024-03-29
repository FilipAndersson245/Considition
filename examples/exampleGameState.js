const a = {
  code: 200, //Http status code
  success: true, //Indicates that the request was successfull
  gameState: {
    gameId: '5c62ebb6-8739-4116-849c-fd11a28ebb3a', //Id of the current gamestate
    gameStatus: 'running', // Indicates if the game is currently running, waiting for players, or finished.
    turn: 105, //The current turn
    yourPlayer: {
      xPos: 10, // Position on the x-axis
      yPos: 12, // Position on the y-axis
      status: 'biking', // What your runner is currently doing. See below for possible statuses.
      statusDuration: 0, // Indicates for how long you'll keep being stunned/exhausted
      stamina: 30, // Making moves cost different amounts of stamina. In addition, dynamic factors like weather and powerups can affect how much stamina your player will need to perform a certain move.
      powerupInventory: [
        // A list containing names of powerups your player has collected that can be activated (or dropped) with the powerup-command
        'StaminaSale',
        'Flippers',
        'InvertStreams',
      ],
      name: 'Dave', // Your team name
      playedTurns: 105, // The number of played turns
      activePowerups: [
        // A list of currently active powerups and for how long they will be active
        {
          name: 'Flippers',
          duration: 4,
        },
      ],
    },
    otherPlayers: [
      // Same as above but for your opponents
      {
        xPos: 78,
        yPos: 6,
        status: 'biking',
        statusDuration: 0,
        stamina: 0,
        powerupInventory: ['InvertStreams'],
        name: 'Roger',
        playedTurns: 105,
        activePowerups: [],
      },
    ],
    tileInfo: [
      // The map is represented as a 2D-array consisting of 100x100 tiles which can contain any combination of Type, Weather, Powerup, Waterstream and Elevation. More info below
      [
        {
          type: 'forest',
        },

        ,
        {
          type: 'forest',
          weather: 'rain',
        },
      ],
      [
        {
          type: 'road',
          elevation: {
            direction: 'e',
            amount: 28,
          },
        },

        ,
        {
          type: 'road',
          powerup: {
            name: 'Spikeshoes',
          },
        },

        {
          type: 'water',
          waterstream: {
            direction: 's',
            speed: 15,
          },
        },
      ],
    ],
  },
};
