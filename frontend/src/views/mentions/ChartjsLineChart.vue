<template>
  <b-card no-body>
    <b-card-header>
      <div>
        <b-card-title class="mb-1">
          Statistik
        </b-card-title>
        <b-card-sub-title>Analisis Sentimen</b-card-sub-title>
      </div>
    </b-card-header>

    <!-- chart -->
    <b-card-body>
      <chartjs-component-line-chart
        :height="400"
        :data="datacollection.lineChart.data"
        :options="options"
        :plugins="plugins"
      />
    </b-card-body>
  </b-card>
</template>

<script>
import {
  BCard, BCardHeader, BCardBody, BCardSubTitle, BCardTitle,
} from 'bootstrap-vue'
import axios from 'axios'
import { $themeColors } from '@themeConfig'
import ChartjsComponentLineChart from './ChartjsComponentLineChart.vue'

const chartColors = {
  primaryColorShade: '#836AF9',
  yellowColor: '#ffe800',
  successColorShade: '#28dac6',
  warningColorShade: '#ffe802',
  warningLightColor: '#FDAC34',
  infoColorShade: '#299AFF',
  greyColor: '#4F5D70',
  blueColor: '#2c9aff',
  blueLightColor: '#84D0FF',
  greyLightColor: '#EDF1F4',
  tooltipShadow: 'rgba(0, 0, 0, 0.25)',
  lineChartPrimary: '#666ee8',
  lineChartDanger: '#ff4961',
  labelColor: '#6e6b7b',
  grid_line_color: 'rgba(200, 200, 200, 0.2)',
}
/* eslint-disable func-names, no-param-reassign */
export default {
  components: {
    BCard,
    BCardHeader,
    BCardBody,
    BCardSubTitle,
    BCardTitle,
    ChartjsComponentLineChart,
  },
  data() {
    return {
      datacollection: null,
      plugins: [
        // to add spacing between legends and chart
        {
          beforeInit(chart) {
            chart.legend.afterFit = function () {
              this.height += 20
            }
          },
        },
      ],
      options: {
        responsive: true,
        maintainAspectRatio: false,
        backgroundColor: false,
        hover: {
          mode: 'label',
        },
        tooltips: {
          // Updated default tooltip UI
          shadowOffsetX: 1,
          shadowOffsetY: 1,
          shadowBlur: 8,
          shadowColor: chartColors.tooltipShadow,
          backgroundColor: $themeColors.white,
          titleFontColor: $themeColors.black,
          bodyFontColor: $themeColors.black,
        },
        layout: {
          padding: {
            top: -15,
            bottom: -25,
            left: -15,
          },
        },
        scales: {
          xAxes: [
            {
              display: true,
              scaleLabel: {
                display: true,
              },
              gridLines: {
                display: true,
                color: chartColors.grid_line_color,
                zeroLineColor: chartColors.grid_line_color,
              },
              ticks: {
                fontColor: chartColors.labelColor,
              },
            },
          ],
          yAxes: [
            {
              display: true,
              scaleLabel: {
                display: true,
              },
              ticks: {
                stepSize: 100,
                min: 0,
                max: 400,
                fontColor: chartColors.labelColor,
              },
              gridLines: {
                display: true,
                color: chartColors.grid_line_color,
                zeroLineColor: chartColors.grid_line_color,
              },
            },
          ],
        },
        legend: {
          position: 'top',
          align: 'start',
          labels: {
            usePointStyle: true,
            padding: 25,
            boxWidth: 9,
          },
        },
      },
    }
  },
  watch: {

  },
  mounted() {
    this.renderChart(this.datacollection)
  },
  created() {
    axios
      .get('http://127.0.0.1:5000/tweet/daytoday?hashtag=bumn')
      .then(
        response => {
          const label = []
          const dataPositive = []
          const dataNegative = []
          for (let i = 0; i < response.data.result.length; i += 1) {
            const result = response.data.result[i]
            if (!label.includes(result.dateLabel)) {
              label.push(result.dateLabel)
            }
            if (result.classification_result === 0) {
              dataNegative.push(parseInt(result.countSentiment, 10))
            } else {
              dataPositive.push(parseInt(result.countSentiment, 10))
            }
          }
          this.datacollection = {
            lineChart: {
              data: {
                labels: label,
                datasets: [
                  {
                    data: dataPositive,
                    label: 'Positif',
                    borderColor: chartColors.lineChartPrimary,
                    lineTension: 0.5,
                    pointStyle: 'circle',
                    backgroundColor: chartColors.lineChartPrimary,
                    fill: false,
                    pointRadius: 1,
                    pointHoverRadius: 5,
                    pointHoverBorderWidth: 5,
                    pointBorderColor: 'transparent',
                    pointHoverBorderColor: $themeColors.white,
                    pointHoverBackgroundColor: chartColors.lineChartPrimary,
                    pointShadowOffsetX: 1,
                    pointShadowOffsetY: 1,
                    pointShadowBlur: 5,
                    pointShadowColor: chartColors.tooltipShadow,
                  },
                  {
                    data: dataNegative,
                    label: 'Negatif',
                    borderColor: chartColors.lineChartDanger,
                    lineTension: 0.5,
                    pointStyle: 'circle',
                    backgroundColor: chartColors.lineChartDanger,
                    fill: false,
                    pointRadius: 1,
                    pointHoverRadius: 5,
                    pointHoverBorderWidth: 5,
                    pointBorderColor: 'transparent',
                    pointHoverBorderColor: $themeColors.white,
                    pointHoverBackgroundColor: chartColors.lineChartDanger,
                    pointShadowOffsetX: 1,
                    pointShadowOffsetY: 1,
                    pointShadowBlur: 5,
                    pointShadowColor: chartColors.tooltipShadow,
                  },
                  {
                    data: [80, 99, 82, 90, 115, 115, 74, 75, 130, 155, 125, 90, 140, 130, 180],
                    label: 'Netral',
                    borderColor: chartColors.warningColorShade,
                    lineTension: 0.5,
                    pointStyle: 'circle',
                    backgroundColor: chartColors.warningColorShade,
                    fill: false,
                    pointRadius: 1,
                    pointHoverRadius: 5,
                    pointHoverBorderWidth: 5,
                    pointBorderColor: 'transparent',
                    pointHoverBorderColor: $themeColors.white,
                    pointHoverBackgroundColor: chartColors.warningColorShade,
                    pointShadowOffsetX: 1,
                    pointShadowOffsetY: 1,
                    pointShadowBlur: 5,
                    pointShadowColor: chartColors.tooltipShadow,
                  },
                ],
              },
            },
          }
          console.log(this.datacollection)
        },
      )
  },
}
</script>
