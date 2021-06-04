<template>
  <div>
    <b-row>
      <b-col
        lg="3"
        sm="6"
      >
        <statistic-card-with-area-chart
          v-if="subscribersGained.analyticsData"
          icon="UsersIcon"
          :statistic="kFormatter(subscribersGained.analyticsData.subscribers)"
          statistic-title="Subscribers Gained"
          :chart-data="subscribersGained.series"
        />
      </b-col>
      <b-col
        lg="3"
        sm="6"
      >
        <statistic-card-with-area-chart
          v-if="revenueGenerated.analyticsData"
          icon="CreditCardIcon"
          color="success"
          :statistic="kFormatter(revenueGenerated.analyticsData.revenue)"
          statistic-title="Revenue Generated"
          :chart-data="revenueGenerated.series"
        />
      </b-col>
      <b-col
        lg="3"
        sm="6"
      >
        <statistic-card-with-area-chart
          v-if="quarterlySales.analyticsData"
          icon="ShoppingCartIcon"
          color="danger"
          :statistic="kFormatter(quarterlySales.analyticsData.sales)"
          statistic-title="Quarterly Sales"
          :chart-data="quarterlySales.series"
        />
      </b-col>
      <b-col
        lg="3"
        sm="6"
      >
        <statistic-card-with-area-chart
          v-if="ordersRecevied.analyticsData"
          icon="PackageIcon"
          color="warning"
          :statistic="kFormatter(ordersRecevied.analyticsData.orders)"
          statistic-title="Orders Received"
          :chart-data="ordersRecevied.series"
        />
      </b-col>
    </b-row>
    <b-row class="match-height">
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
import TimeLine from './TimeLine.vue'
import StatisticCardVertical from '@core/components/statistics-cards/StatisticCardVertical.vue'
import StatisticCardHorizontal from '@core/components/statistics-cards/StatisticCardHorizontal.vue'
import StatisticCardWithAreaChart from '@core/components/statistics-cards/StatisticCardWithAreaChart.vue'
import StatisticCardWithLineChart from '@core/components/statistics-cards/StatisticCardWithLineChart.vue'
import { kFormatter } from '@core/utils/filter'
import ChartjsBarChart from './ChartjsBarChart.vue'
import ChartjsLineChart from './ChartjsLineChart.vue'
import CardStatisticOrderChart from './CardStatisticOrderChart.vue'
import CardStatisticProfitChart from './CardStatisticProfitChart.vue'
import CardStatisticsGroup from './CardStatisticsGroup.vue'
export default {
  components: {
    BRow,
    BCol,

    ChartjsBarChart,
    ChartjsLineChart,
    TimeLine,
    StatisticCardVertical,
    StatisticCardHorizontal,
    StatisticCardWithAreaChart,
    StatisticCardWithLineChart,
    CardStatisticOrderChart,
    CardStatisticProfitChart,
    CardStatisticsGroup,
  },
}
</script>
