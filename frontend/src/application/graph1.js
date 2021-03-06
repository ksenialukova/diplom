import * as React from 'react';
import Paper from '@material-ui/core/Paper';
import {
  Chart,
  ArgumentAxis,
  ValueAxis,
  AreaSeries,
  Title,
  Legend,
} from '@devexpress/dx-react-chart-material-ui';

import { ArgumentScale, Animation } from '@devexpress/dx-react-chart';
import { scalePoint } from 'd3-scale';
import { withStyles } from '@material-ui/core/styles';

const chartRootStyles = {
  chart: {
    paddingRight: '20px',
  },
};
const legendStyles = {
  root: {
    display: 'flex',
    margin: 'auto',
    flexDirection: 'row',
  },
};
const legendLabelStyles = theme => ({
  label: {
    paddingTop: theme.spacing(1),
  },
});
const legendItemStyles = {
  item: {
    flexDirection: 'column',
  },
};

const ChartRootBase = ({ classes, ...restProps }) => (
  <Chart.Root {...restProps} className={classes.chart} />
);
const LegendRootBase = ({ classes, ...restProps }) => (
  <Legend.Root {...restProps} className={classes.root} />
);
const LegendLabelBase = ({ classes, ...restProps }) => (
  <Legend.Label {...restProps} className={classes.label} />
);
const LegendItemBase = ({ classes, ...restProps }) => (
  <Legend.Item {...restProps} className={classes.item} />
);
const ChartRoot = withStyles(chartRootStyles, { name: 'ChartRoot' })(ChartRootBase);
const LegendRoot = withStyles(legendStyles, { name: 'LegendRoot' })(LegendRootBase);
const LegendLabel = withStyles(legendLabelStyles, { name: 'LegendLabel' })(LegendLabelBase);
const LegendItem = withStyles(legendItemStyles, { name: 'LegendItem' })(LegendItemBase);

export default class Demo extends React.PureComponent {
  constructor(props) {
    super(props);

    this.state = {
    };
  }

  render() {
    const { graph1: chartData } = this.props;
    return (
      <Paper>
        {chartData &&
        <Chart
            data={chartData}
            rootComponent={ChartRoot}
        >
          <ArgumentScale factory={scalePoint}/>
          <ArgumentAxis/>
          <ValueAxis/>

          <AreaSeries
              name="Вартість перевезень розрахованих методом найближчого сусіда"
              valueField="neighbour"
              argumentField="date"
          />
          <AreaSeries
              name="Вартість перевезень розрахованих методом бджолиних колоній"
              valueField="bees"
              argumentField="date"
          />
          <Animation/>
          <Legend
              position="bottom"
              rootComponent={LegendRoot}
              itemComponent={LegendItem}
              labelComponent={LegendLabel}
          />
          <Title
              text="Порівняння вартостей"
          />
        </Chart>
        }
      </Paper>
    );
  }
}
