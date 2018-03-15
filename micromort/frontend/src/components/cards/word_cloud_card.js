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
import filter from 'lodash/filter';
import lodashmap from 'lodash/map';

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
     this.handleChipClick = this.handleChipClick.bind(this);

  }


  render() {
      const { classes, chipData } = this.props;
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
                  data={this.props.wordCloudData}
                  fontSizeMapper={fontSizeMapper}
                  rotate={rotate}
                  width={450}
                  height={350}
                  />
                </div>
            </CardContent>

            <div className={classes.actions}>
              {
                chipData.map(data => {
                  return (
                    <CustomChip
                      key={data.key}
                      text={data.label}
                      isSelected={data.selected}
                      onClick={this.handleChipClick}
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

  handleChipClick(key){
    var chipData = this.props.chipData.slice();
    const that = this;
    chipData.forEach(chipInfo =>{
      if (chipInfo.key === key) {
        chipData[key]["selected"] = !chipData[key]["selected"]
      }
    })

    this.props.onChipClick(chipData)

    //Get the appropriate cloud data as well
  }

}

export default withStyles(tagCloudStyles)(TagCloudCard)
