import React from 'react';
import { withStyles } from 'material-ui/styles';
import PropTypes from 'prop-types';
import Card, { CardHeader, CardContent, CardActions } from 'material-ui/Card';
import WordCloud from 'react-d3-cloud';
import Avatar from 'material-ui/Avatar';
import Share from 'material-ui-icons/Share';
import WordCloudIcon from '../icons/word_cloud_icon';
import { tagCloudStyles } from '../../configs/styles';
import  CustomChip  from '../custom_chip'

const data = [
  { text: 'Hey', value: 1000 },
  { text: 'lol', value: 200 },
  { text: 'first impression', value: 800 },
  { text: 'very cool', value: 1000000 },
  { text: 'duck', value: 10 },
];

const fontSizeMapper = word => Math.log2(word.value) * 5;
const rotate = word => word.value % 360;



class TagCloudCard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        chipData: [
          { key: 0, label: 'Health', selected: true },
          { key: 1, label: 'Safety', selected: false },
          { key: 2, label: 'Environment', selected: false },
          { key: 3, label: 'Social Relations', selected: false },
          { key: 4, label: 'Meaning in Life', selected: false },
          { key: 5, label: 'Achievements', selected: false },
          { key: 6, label: 'Economics', selected: false },
        ],
        wordCloudData: data

     };
     this.onChipClick = this.onChipClick.bind(this);

  }
  render() {
      const { classes } = this.props;
      return (
        <div className={classes.container}>
          <Card>
            <CardHeader
              avatar={
                <Avatar classes={{
                  root: classes.root
                }}>
                  <WordCloudIcon
                    color="error"
                    style={{
                      width: 30,
                      height: 30,
                    }}>

                  </WordCloudIcon>
                </Avatar>
              }
              title="Word Cloud"
              classes={{
                title: classes.cardHeaderTitle
              }}
            />
            <CardContent>
              <div>
                <WordCloud
                  data={this.state.wordCloudData}
                  fontSizeMapper={fontSizeMapper}
                  rotate={rotate}
                  width={450}
                  height={350}
                  />
                </div>
            </CardContent>

            <div className={classes.actions}>
              {
                this.state.chipData.map(data => {
                  return (
                    <CustomChip
                      key={data.key}
                      text={data.label}
                      isSelected={data.selected}
                      onClick={this.onChipClick}
                      chipNumber={data.key}>

                    </CustomChip>
                  );
                })
              }
            </div>

          </Card>
        </div>
    );
  }

  onChipClick(key){
    var chipData = this.state.chipData.slice()
    chipData.forEach(chipInfo =>{
      if (chipInfo.key === key) {
        chipData[key]["selected"] = !chipData[key]["selected"]
      }
    })
    this.setState({
      chipData: chipData
    })

    //Get the appropriate cloud data as well
  }
}

export default withStyles(tagCloudStyles)(TagCloudCard)
