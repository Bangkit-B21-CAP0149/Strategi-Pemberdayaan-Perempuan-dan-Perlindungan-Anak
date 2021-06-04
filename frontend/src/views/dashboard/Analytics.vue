<template>
  <section id="dashboard">
    <b-row class="match-height">
      <b-col
        lg="6"
        md="12"
      >
        <analytics-welcome />
      </b-col>
    </b-row>
  </section>
</template>

<script>
import { BRow, BCol } from 'bootstrap-vue'

import { kFormatter } from '@core/utils/filter'
import AnalyticsWelcome from './AnalyticsWelcome.vue'

export default {
  components: {
    BRow,
    BCol,
    AnalyticsWelcome,
  },
  methods: {
    kFormatter,
  },
}
</script>
