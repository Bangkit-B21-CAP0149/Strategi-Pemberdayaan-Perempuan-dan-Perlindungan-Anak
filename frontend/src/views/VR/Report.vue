<template>
  <b-card-code
    title="Custom data rendering"
    no-body
  >
    <b-table
      small
      :fields="fields"
      :items="items"
      responsive="sm"
    >

      <template #cell(index)="data">
        {{ data.index + 1 }}
      </template>

      <template #cell(risk_level)="data">
        <div v-if="data.value === 'Higher Risk'">
          <b-badge
            pill
            variant="danger"
          >Higher Risk
          </b-badge>
        </div>
        <div v-else-if="data.value === 'Mid Risk'">
          <b-badge
            pill
            variant="warning"
          >Higher Risk
          </b-badge>
        </div>
        <div v-else>
          <b-badge
            pill
            variant="success"
          >Low Risk
          </b-badge>
        </div>
      </template>
    </b-table>

    <template #code>
      {{ codeDataRendering }}
    </template>
  </b-card-code>
</template>

<script>
import axios from 'axios'
import BCardCode from '@core/components/b-card-code/BCardCode.vue'
import { BTable, BBadge } from 'bootstrap-vue'

export default {
  components: {
    BTable,
    BCardCode,
    BBadge,
  },
  data() {
    return {
      fields: [
        // A virtual column that doesn't exist in items
        'index',
        // A column that needs custom formatting
        { key: 'nik', label: 'NIK' },
        { key: 'date_log', label: 'Date' },
        { key: 'violence_type', label: 'Violence Type' },
        { key: 'relation', label: 'Relation' },
        { key: 'victim_age', label: 'Victim Age' },
        { key: 'agressor_age', label: ' Agressor Age' },
        { key: 'prev_abuse_report', label: 'Prev Abuse Report' },
        { key: 'living_together', label: 'Living Together' },
        { key: 'short_chronology', label: 'Chronology' },
        { key: 'relation', label: 'Relation' },
        { key: 'risk_level', label: 'Risk Level' },
      ],
      items: null,
    }
  },
  created() {
    axios
      .get('http://34.136.214.191:5001/vr/list_report')
      .then(
        response => {
          this.items = response.data.result
        },
      )
  },
}
</script>
