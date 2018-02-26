// This is where all the styles for difference components go in

/**************************************
*         STYLES FOR APPGRID          *
**************************************/
const appGridStyles = {
}


/**************************************
*         STYLES FOR SIDEDRAWER       *
**************************************/

const navigationDrawerStyles = theme => (
  {
      drawerPaper: {
        height: '100%',
        position: 'relative',

      },
      drawerHeader: theme.mixins.toolbar,
      projectLogo: {
        display: 'table',
        'font-size': '2em',
        'margin-top': '12px',
        'margin-left': 'auto',
        'margin-right': 'auto'

      }
  }
)

const navigationDrawerItemStyles = {
  unselectedText: {
    "font-family": "Roboto, Helvetica",
    "font-size ": "1rem",
    "font-weight": 400,
    "line-height": "1.5em",
    color: 'gray'
  },
  selectedText: {
    "font-family": "Roboto, Helvetica",
    "font-size": "1rem",
    "font-weight": 600,
    "line-height": "1.5em",
    color: 'black',
  },
  item: {
      position: 'relative',
      display: 'block',
      textDecoration: 'none',
  },
}

/**************************************
*         STYLES FOR APPBAR       *
**************************************/
const appBarStyles = {
  root: {
    position: 'relative'
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20
  }
}

/**************************************
*         STYLES FOR DATEVIEW       *
**************************************/

const dateViewStyles = {
  root: {
    'margin-top': '3%',
    'margin-left': '3%'
  }
}

/**************************************
*         STYLES FOR TAGCLOUD CARD     *
**************************************/
const tagCloudStyles = {
  container: {
    display: 'flex',
    'flex-direction': 'row',
    'flex-wrap': 'nowrap',
    'margin-top': '20px'
  },
  root: {
    'background-color': '#e3e3e3',
    'justify-content': 'flex-end',
    'align-items': 'flex-end'
  },
  cardHeaderTitle: {
    'font-family': "Roboto, Helvetica, Arial, sans-serif",
    'font-weight': 550,
    'font-size': '1.2em',
    "line-height": '0.85em',
    "color": 'rgba(0, 0, 0, 0.85)',
    'font-variant': 'small-caps'
  },
  actions: {
    display: 'flex',
    'justifyContent': 'center',
    'flexWrap': 'wrap',
    'padding-bottom': '10px'
  },
  'chip': {
    'margin-top': '10px',
    'margin-right': '4px'
  },
  'chip-selected': {
    'margin-top': '10px',
    'margin-right': '4px',
    'background-color': 'green'
  }

}


module.exports = {
  appBarStyles,
  appGridStyles,
  dateViewStyles,
  navigationDrawerStyles,
  navigationDrawerItemStyles,
  tagCloudStyles
}
