"""Static Query for the server"""

GET_NODE = """
query GetNode($network: String!, $node_id: String!){
  getNode(network: $network, node_id: $node_id) {
    version
    node_id
    alias
    color
    network
    address {
      type
      host
      port
    } 
    os_info {
      os
      version
      architecture
    }
    node_info {
      implementation
      version
    }
    timezone
    last_update
  }
}
"""

GET_NODES = """
query GetNodes($network: String!){
  getNodes(network: $network) {
    version
    node_id
    alias
    color
    network
    address {
      type
      host
      port
    } 
    os_info {
      os
      version
      architecture
    }
    node_info {
      implementation
      version
    }
    timezone
    last_update
  }
}
"""

GET_METRIC_ONE = """
query MetricOne($network: String!, $node_id: String!, $first: Int!, $last: Int!){
  metricOne(network: $network,  node_id: $node_id, first: $first, last: $last) {
    page_info {
      start
      end
      has_next
    }
    channels_info {
      node_id
      channel_id
      node_alias
      color
      capacity
      forwards {
        direction
        status
        failure_reason
        failure_code
        timestamp
      }
      up_time {
        event
        status
        timestamp
      }
      online
      last_update
      direction
      fee {
        base
        per_msat
      }
      limits {
        min
        max
      }
    }
    up_time {
      event
      channels {
        tot_channels
        summary {
          node_id
          alias
          color
          channel_id
          state
        }
      }
      forwards {
        completed
        failed
      }
      timestamp
      fee {
        base
        per_msat
      }
      limits {
        min
        max
      }
    }
  }
}
"""

LOCAL_SCORE_OUTPUT = """
query LocalScoreOutput($network: String!, $node_id: String!) {
  getMetricOneResult(network: $network, node_id: $node_id) {
    age
    last_update
    version
    up_time {
      one_day
      ten_days
      thirty_days
      six_months
    }
    forwards_rating {
      one_day {
        success
        failure
        local_failure
      }
      ten_days {
        success
        failure
        local_failure
      }
      thirty_days {
        success
        failure
        local_failure
      }
      six_months {
        success
        failure
        local_failure
      }
      full {
        success
        failure
        local_failure
      }
    }
    channels_info {
      node_id
      alias
      channel_id
      capacity
      direction
      up_time {
        one_day
        ten_days
        thirty_days
        six_months
        full
      }
      forwards_rating {
      one_day {
        success
        failure
        local_failure
      }
        thirty_days {
        success
        failure
        local_failure
      }
        six_months {
        success
        failure
        local_failure
      }
      full {
          success
          failure
          local_failure
        }
      }
    }
  }
}
"""
