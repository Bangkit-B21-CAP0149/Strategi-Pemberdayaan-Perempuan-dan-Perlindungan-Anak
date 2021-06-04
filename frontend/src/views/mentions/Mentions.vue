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
          :statistic="this.abnumber(item.total_mentions)"
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
          statistic-title="Positif"
          :statistic="this.abnumber(item.total_positif)"
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
          :statistic="this.abnumber(item.total_negatif)"
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
          :statistic="this.abnumber(item.total_netral)"
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
          :statistic="this.abnumber(item.total_retweet)"
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
          :statistic="this.abnumber(item.total_likes)"
          statistic-title="Likes"
        />
      </b-col>
      <b-col
        xl="2"
        md="4"
        sm="6"
      >
        <statistic-card-vertical
          hide-chart
          color="secondary"
          icon="UsersIcon"
          :statistic="this.abnumber(item.total_profile)"
          statistic-title="Total Profile"
        />
      </b-col>
      <b-col
        xl="2"
        md="4"
        sm="6"
      >
        <statistic-card-vertical
          hide-chart
          color="primary"
          icon="TwitterIcon"
          :statistic="this.abnumber(item.total_tweet)"
          statistic-title="Total Tweet"
        />
      </b-col>
      <b-col
        xl="2"
        md="4"
        sm="6"
      >
        <statistic-card-vertical
          hide-chart
          color="info"
          icon="ActivityIcon"
          :statistic="this.abnumber(item.total_reaction)"
          statistic-title="Total Reaction"
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
import axios from 'axios'
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
  data() {
    return {
      data: null,
    }
  },
  created() {
    axios
      .get('http://34.136.214.191:5001/sentiment/summary/palestina')
      .then(
        response => {
          this.item = response.data.result
        },
      )
  },
  methods: {
    abnumber(value) {
      const suffixes = ['', 'k', 'jt', 'm', 't']
      const suffixNum = Math.floor((`${value}`).length / 3)
      const shortValue = parseFloat((suffixNum !== 0 ? (value / 1000 ** suffixNum) : value).toPrecision(2))
      if (shortValue % 1 !== 0) {
        this.shortValue = shortValue.toFixed(0)
      }
      return shortValue + suffixes[suffixNum]
    },
  },
}

</script>
