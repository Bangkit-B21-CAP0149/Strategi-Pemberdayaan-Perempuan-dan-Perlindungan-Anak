<template>
  <div>
    <b-row class="match-height">
      <b-col
        xl="2"
        md="4"
        sm="6"
      >
        <statistic-card-vertical
          icon="EyeIcon"
          statistic="36.9k"
          statistic-title="Mentions"
          color="info"
        />
      </b-col>
      <b-col
        xl="2"
        md="4"
        sm="6"
      >
        <statistic-card-vertical
          color="success"
          icon="ArrowUpRightIcon"
          statistic="12k"
          statistic-title="Positif"
        />
      </b-col>
      <b-col
        xl="2"
        md="4"
        sm="6"
      >
        <statistic-card-vertical
          color="danger"
          icon="ArrowDownLeftIcon"
          statistic="97.8k"
          statistic-title="Negatif"
        />
      </b-col>
      <b-col
        xl="2"
        md="4"
        sm="6"
      >
        <statistic-card-vertical
          color="warning"
          icon="ArrowRightIcon"
          statistic="26.8"
          statistic-title="Netral"
        />
      </b-col>
      <b-col
        xl="2"
        md="4"
        sm="6"
      >
        <statistic-card-vertical
          color="primary"
          icon="CornerDownRightIcon"
          statistic="689"
          statistic-title="Retweet"
        />
      </b-col>
      <b-col
        xl="2"
        md="4"
        sm="6"
      >
        <statistic-card-vertical
          hide-chart
          color="danger"
          icon="HeartIcon"
          statistic="2.1k"
          statistic-title="Likes"
        />
      </b-col>
    </b-row>
    <b-row class="match-height">
      <b-col cols="12">
        <apex-line-chart />
      </b-col>
      <b-col cols="12">
        <chartjs-line-chart />
      </b-col>
    </b-row>
    <b-row>
      <b-col lg="6">
        <b-row class="match-height">
          <b-col md="12">
            <time-line />
          </b-col>
        </b-row>
      </b-col>
      <b-col lg="6">
        <chartjs-bar-chart />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { BRow, BCol } from 'bootstrap-vue'
import StatisticCardVertical from '@core/components/statistics-cards/StatisticCardVertical.vue'
import ApexLineChart from './ApexLineChart.vue'
import TimeLine from './TimeLine.vue'
import ChartjsBarChart from './ChartjsBarChart.vue'
import ChartjsLineChart from './ChartjsLineChart.vue'

export default {
  components: {
    BRow,
    BCol,
    ApexLineChart,
    ChartjsBarChart,
    ChartjsLineChart,
    TimeLine,
    StatisticCardVertical,
  },
}
</script>
