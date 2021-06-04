<template>
  <b-card no-body>
    <b-card-header>
      <!-- title and subtitle -->
      <div>
        <b-card-title class="mb-1">
          Pencapaian
        </b-card-title>
        <b-card-sub-title>Total Tweet Setiap Hari</b-card-sub-title>
      </div>
      <!--/ title and subtitle -->

      <!-- badge -->
      <div class="d-flex align-items-center flex-wrap mt-sm-0 mt-1">
        <h5 class="font-weight-bolder mb-0 mr-1">
          $ 100,000
        </h5>
        <b-badge variant="light-secondary">
          <feather-icon
            icon="ArrowDownIcon"
            size="16"
            class="text-danger mr-25"
          />
          <span class="align-middle">20%</span>
        </b-badge>
      </div>
      <!--/ badge -->
    </b-card-header>

    <b-card-body>
      <vue-apex-charts
        type="line"
        height="400"
        :options="datacollection.lineChartSimple.chartOptions"
        :series="datacollection.lineChartSimple.series"
      />
    </b-card-body>
  </b-card>
</template>

<script>
import axios from 'axios'
import { $themeColors } from '@themeConfig'
import {
  BCard, BCardBody, BCardHeader, BCardTitle, BCardSubTitle, BBadge,
} from 'bootstrap-vue'
import VueApexCharts from 'vue-apexcharts'

export default {
  components: {
    VueApexCharts,
    BCardHeader,
    BCard,
    BBadge,
    BCardBody,
    BCardTitle,
    BCardSubTitle,
  },
  data() {
    return {
      datacollection: null,
    }
  },
  created() {
    axios
      .get('http://127.0.0.1:5000/tweet/countall')
      .then(
        response => {
          const label = []
          const counted = []
          for (let i = 0; i < response.data.result.length; i += 1) {
            const result = response.data.result[i]
            label.push(result.dateLabel)
            counted.push(parseInt(result.countall, 10))
          }
          this.datacollection = {
            lineChartSimple: {
              series: [
                {
                  data: counted,
                },
              ],
              chartOptions: {
                chart: {
                  zoom: {
                    enabled: false,
                  },
                  toolbar: {
                    show: false,
                  },
                },
                markers: {
                  strokeWidth: 7,
                  strokeOpacity: 1,
                  strokeColors: [$themeColors.light],
                  colors: [$themeColors.warning],
                },
                colors: [$themeColors.warning],
                dataLabels: {
                  enabled: false,
                },
                stroke: {
                  curve: 'straight',
                },
                grid: {
                  xaxis: {
                    lines: {
                      show: true,
                    },
                  },
                },
                tooltip: {
                  custom(data) {
                    return `${'<div class="px-1 py-50"><span>'}${
                      data.series[data.seriesIndex][data.dataPointIndex]
                    } Tweet</span></div>`
                  },
                },
                xaxis: {
                  categories: label,
                },
                yaxis: {
                  // opposite: isRtl,
                },
              },
            },
          }
        },
      )
  },
}
</script>
