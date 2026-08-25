import { useEffect, useState } from "react"
import "./App.css"
import {
  AnalysisPage,
  DataCenterPage,
  GlobalFilterBar,
  HelpPanel,
  NotificationsPanel,
  ProfileMenu,
  ReportsPage,
  SettingsDrawer,
  StatisticsPage,
  TimeScopeTabs,
  ToolsPage
} from "./ManagementPages"


// 1. 本地会话存储
const SESSION_STORAGE_KEY =
  "restaurant-analysis-agent-session"


const loadSession = () => {
  try {
    const savedSession = localStorage.getItem(
      SESSION_STORAGE_KEY
    )

    if (!savedSession) {
      return null
    }

    return JSON.parse(
      savedSession
    )
  } catch (error) {
    console.error(
      "读取本地会话失败:",
      error
    )

    return null
  }
}


const UI_SETTINGS_KEY =
  "restaurant-analysis-ui-settings"


const loadUiSettings = () => {
  try {
    const savedSettings = localStorage.getItem(
      UI_SETTINGS_KEY
    )

    return savedSettings
      ? JSON.parse(savedSettings)
      : {
          compact: false,
          animations: true
        }
  } catch (error) {
    console.error(
      "读取界面设置失败:",
      error
    )

    return {
      compact: false,
      animations: true
    }
  }
}
// 2. SaaS 经营分析后台
function App() {
  const [question, setQuestion] = useState("")
  const [aiOpen, setAiOpen] = useState(false)
  const [loading, setLoading] = useState(false)

  const [activePage, setActivePage] = useState("home")

  const [dashboardData, setDashboardData] = useState(null)
  const [dashboardLoading, setDashboardLoading] = useState(true)
  const [dashboardError, setDashboardError] = useState("")


  const [storeData, setStoreData] = useState(null)
  const [storeLoading, setStoreLoading] = useState(true)
  const [storeError, setStoreError] = useState("")

  const [selectedStoreId, setSelectedStoreId] = useState("")
  const [selectedStoreCategory, setSelectedStoreCategory] = useState("")
  const [selectedStoreDistrict, setSelectedStoreDistrict] = useState("")
  const [storeMetric, setStoreMetric] = useState("total_sales")

  const [analyticsData, setAnalyticsData] = useState(null)
  const [analyticsLoading, setAnalyticsLoading] = useState(true)
  const [analyticsError, setAnalyticsError] = useState("")
  const [analyticsRefreshKey, setAnalyticsRefreshKey] = useState(0)

  const [globalStoreId, setGlobalStoreId] = useState("")
  const [globalCategory, setGlobalCategory] = useState("")
  const [globalProductId, setGlobalProductId] = useState("")
  const [globalMetric, setGlobalMetric] = useState("total_sales")
  const [timeScope, setTimeScope] = useState(1)
  const [businessAnalysisTab, setBusinessAnalysisTab] = useState("products")

  const [helpOpen, setHelpOpen] = useState(false)
  const [notificationsOpen, setNotificationsOpen] = useState(false)
  const [profileOpen, setProfileOpen] = useState(false)
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [uiSettings, setUiSettings] = useState(loadUiSettings)

  // 3. 恢复本地会话
  const [messages, setMessages] = useState(
    () => {
      const savedSession = loadSession()

      return savedSession?.messages || [
        {
          role: "assistant",
          content: "你好，我是经营数据分析助手，有什么可以帮你？"
        }
      ]
    }
  )

  const [
    conversationHistory,
    setConversationHistory
  ] = useState(
    () =>
      loadSession()?.conversationHistory
      || []
  )

  const [
    structuredContext,
    setStructuredContext
  ] = useState(
    () =>
      loadSession()?.structuredContext
      || {}
  )

  const [
    structuredMemory,
    setStructuredMemory
  ] = useState(
    () =>
      loadSession()?.structuredMemory
      || []
  )

  // 4. 持久化当前会话
  useEffect(() => {
    const session = {
      messages,
      conversationHistory,
      structuredContext,
      structuredMemory
    }

    localStorage.setItem(
      SESSION_STORAGE_KEY,
      JSON.stringify(session)
    )
  }, [
    messages,
    conversationHistory,
    structuredContext,
    structuredMemory
  ])

  // 5. 加载 Dashboard 真实数据
  useEffect(() => {
    let active = true

    const loadDashboardData = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8001/api/dashboard"
        )

        if (!response.ok) {
          throw new Error(
            `HTTP ${response.status}`
          )
        }

        const data = await response.json()

        if (!data.success) {
          throw new Error(
            data.message || "Dashboard 数据加载失败"
          )
        }

        if (active) {
          setDashboardData(data)
          setDashboardError("")
        }
      } catch (error) {
        console.error(
          "Dashboard 数据请求失败:",
          error
        )

        if (active) {
          setDashboardError(
            "Dashboard 数据加载失败"
          )
        }
      } finally {
        if (active) {
          setDashboardLoading(false)
        }
      }
    }

    loadDashboardData()

    return () => {
      active = false
    }
  }, [])




  // 6A. 加载门店真实数据
  useEffect(() => {
    let active = true

    const loadStoreData = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8001/api/stores"
        )

        if (!response.ok) {
          throw new Error(
            `HTTP ${response.status}`
          )
        }

        const data = await response.json()

        if (!data.success) {
          throw new Error(
            data.message || "门店数据加载失败"
          )
        }

        if (active) {
          setStoreData(data)
          setStoreError("")
        }
      } catch (error) {
        console.error(
          "门店数据请求失败:",
          error
        )

        if (active) {
          setStoreError(
            "门店数据加载失败"
          )
        }
      } finally {
        if (active) {
          setStoreLoading(false)
        }
      }
    }

    loadStoreData()

    return () => {
      active = false
    }
  }, [])

  // 6B. 加载全局筛选聚合数据
  useEffect(() => {
    let active = true

    const loadAnalyticsData = async () => {
      setAnalyticsLoading(true)

      const parameters = new URLSearchParams({
        months: String(timeScope)
      })

      if (globalStoreId) {
        parameters.set("store_id", globalStoreId)
      }

      if (globalCategory) {
        parameters.set("category", globalCategory)
      }

      if (globalProductId) {
        parameters.set("product_id", globalProductId)
      }

      try {
        const response = await fetch(
          `http://127.0.0.1:8001/api/analytics?${parameters.toString()}`
        )

        if (!response.ok) {
          throw new Error(
            `HTTP ${response.status}`
          )
        }

        const data = await response.json()

        if (!data.success) {
          throw new Error(
            data.message || "筛选经营数据加载失败"
          )
        }

        if (active) {
          setAnalyticsData(data)
          setAnalyticsError("")
        }
      } catch (error) {
        console.error(
          "筛选经营数据请求失败:",
          error
        )

        if (active) {
          setAnalyticsError(
            "筛选经营数据加载失败"
          )
        }
      } finally {
        if (active) {
          setAnalyticsLoading(false)
        }
      }
    }

    loadAnalyticsData()

    return () => {
      active = false
    }
  }, [
    globalStoreId,
    globalCategory,
    globalProductId,
    timeScope,
    analyticsRefreshKey
  ])

  // 6C. 持久化界面设置
  useEffect(() => {
    localStorage.setItem(
      UI_SETTINGS_KEY,
      JSON.stringify(uiSettings)
    )
  }, [uiSettings])

  // 7. 开始新会话
  const handleNewSession = () => {
    const confirmed = window.confirm(
      "确定开始新会话吗？当前聊天记录将被清空。"
    )

    if (!confirmed) {
      return
    }

    setQuestion("")

    setMessages([
      {
        role: "assistant",
        content: "你好，我是经营数据分析助手，有什么可以帮你？"
      }
    ])

    setConversationHistory([])
    setStructuredContext({})
    setStructuredMemory([])
  }

  // 8. 提交 AI 问题
  const handleSubmit = async (event) => {
    event.preventDefault()

    const currentQuestion = question.trim()

    if (!currentQuestion || loading) {
      return
    }

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: currentQuestion
      }
    ])

    setQuestion("")
    setLoading(true)

    try {
      const response = await fetch(
        "http://127.0.0.1:8001/api/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            question: currentQuestion,
            conversation_history: conversationHistory,
            structured_context: structuredContext,
            structured_memory: structuredMemory
          })
        }
      )

      if (!response.ok) {
        throw new Error(
          `HTTP ${response.status}`
        )
      }

      const data = await response.json()

      // 9. 保存后端返回的多轮上下文
      setConversationHistory(
        data.conversation_history || []
      )

      setStructuredContext(
        data.structured_context || {}
      )

      setStructuredMemory(
        data.structured_memory || []
      )

      // 10. 显示 AI 回答
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: data.answer || "暂时没有返回结果。"
        }
      ])
    } catch (error) {
      console.error(
        "请求失败:",
        error
      )

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: "请求失败，请确认后端服务是否正常运行。"
        }
      ])
    } finally {
      setLoading(false)
    }
  }



  // 10A. 通用页面交互
  const navigateToPage = (page) => {
    setActivePage(page)
    setNotificationsOpen(false)
    setProfileOpen(false)
  }

  const handleGlobalFilterChange = (
    field,
    value
  ) => {
    if (field === "storeId") {
      setGlobalStoreId(value)
    } else if (field === "category") {
      setGlobalCategory(value)
    } else if (field === "productId") {
      setGlobalProductId(value)
    } else if (field === "metric") {
      setGlobalMetric(value)
    }
  }

  const resetGlobalFilters = () => {
    setGlobalStoreId("")
    setGlobalCategory("")
    setGlobalProductId("")
    setGlobalMetric("total_sales")
  }

  const refreshAnalytics = () => {
    setAnalyticsRefreshKey(
      (current) => current + 1
    )
  }

  const handleUiSettingChange = (
    field,
    value
  ) => {
    setUiSettings((current) => ({
      ...current,
      [field]: value
    }))
  }

  const openSettings = () => {
    setSettingsOpen(true)
    setProfileOpen(false)
  }

  const globalFilterValues = {
    storeId: globalStoreId,
    category: globalCategory,
    productId: globalProductId,
    metric: globalMetric
  }

  const businessCapabilities = [
    {
      tab: "products",
      type: "商品销售",
      capability: "商品销售额 / 销量 / 多商品对比",
      range: "月份 / 全周期"
    },
    {
      tab: "stores",
      type: "门店经营",
      capability: "门店营业额 / 订单 / 客单价排行",
      range: "指定周期"
    },
    {
      tab: "categories",
      type: "门店品类",
      capability: "品类营业额及排名",
      range: "指定周期"
    },
    {
      tab: "aov",
      type: "客单价",
      capability: "当前值 / 上期 / 变化率",
      range: "最近周期"
    }
  ]
  const visibleBusinessCapabilities = (
    businessCapabilities.filter(
      (item) => item.tab === businessAnalysisTab
    )
  )
  // 11. Dashboard 展示数据
  const legacySummary = dashboardData?.summary || {}
  const legacyTrend = dashboardData?.trend || []
  const hasGlobalDataFilters = Boolean(
    globalStoreId
    || globalCategory
    || globalProductId
    || timeScope !== 1
  )
  const useFilteredAnalytics = Boolean(
    analyticsData
    && (
      hasGlobalDataFilters
      || globalMetric === "total_quantity"
    )
  )
  const analyticsSummary = analyticsData?.summary || {}
  const summary = useFilteredAnalytics
    ? {
        ...analyticsSummary,
        top_category: analyticsSummary.top_category?.category,
        top_category_sales: analyticsSummary.top_category?.total_sales,
        sales_change_rate: (
          analyticsSummary.sales_change_rate
        ),
        order_change_rate: (
          analyticsSummary.order_change_rate
        ),
        aov_change_rate: (
          analyticsSummary.aov_change_rate
        )
      }
    : legacySummary
  const trend = useFilteredAnalytics
    ? analyticsData.trend || []
    : legacyTrend
  const periodLabel = (
    useFilteredAnalytics
      ? analyticsData?.period?.label
      : dashboardData?.period?.label
  ) || "最新周期"
  const latestDataDate = (
    analyticsData?.latest_data_date
    || dashboardData?.latest_data_date
    || "--"
  )

  const dashboardMetricOptions = [
    {
      value: "total_sales",
      label: "营业额",
      unit: "currency",
      digits: 0
    },
    {
      value: "order_count",
      label: "订单量",
      unit: "order",
      digits: 0
    },
    {
      value: "avg_order_value",
      label: "客单价",
      unit: "currency",
      digits: 2
    },
    {
      value: "total_quantity",
      label: "销量",
      unit: "quantity",
      digits: 0
    }
  ]
  const dashboardMetricConfig = (
    dashboardMetricOptions.find(
      (option) => option.value === globalMetric
    ) || dashboardMetricOptions[0]
  )

  const productRankingSource = (
      analyticsData?.product_ranking
      || []
  )
  const productRanking = [
    ...productRankingSource
  ].sort((left, right) => (
    (Number(right[globalMetric]) || 0)
    - (Number(left[globalMetric]) || 0)
    || left.product_name.localeCompare(
      right.product_name,
      "zh-CN"
    )
  ))
  const productSummary = analyticsData
    ? {
        total_products: productRanking.length,
        total_sales: analyticsSummary.total_sales,
        total_quantity: analyticsSummary.total_quantity,
        top_product: analyticsSummary.top_product?.product_name,
        top_product_sales: analyticsSummary.top_product?.total_sales
      }
    : {}

  const formatNumber = (
    value,
    digits = 0
  ) => {
    if (
      value === null
      || value === undefined
    ) {
      return "--"
    }

    return Number(value).toLocaleString(
      "zh-CN",
      {
        minimumFractionDigits: digits,
        maximumFractionDigits: digits
      }
    )
  }

  const formatDashboardMetric = (value) => {
    if (dashboardMetricConfig.unit === "currency") {
      return `¥${formatNumber(value, dashboardMetricConfig.digits)}`
    }

    if (dashboardMetricConfig.unit === "order") {
      return `${formatNumber(value)} 单`
    }

    return `${formatNumber(value)} 件`
  }

  const formatRate = (value) => {
    if (
      value === null
      || value === undefined
    ) {
      return timeScope === 3
        ? "所选三个月汇总"
        : "暂无上月数据"
    }

    const number = Number(value)
    const sign = number > 0 ? "+" : ""

    return (
      `较上月 ${sign}${number.toFixed(2)}%`
    )
  }

  const maxMetricValue = trend.length
    ? Math.max(
        ...trend.map(
          (item) => Number(item[globalMetric]) || 0
        )
      )
    : 0

  const chartScaleMax = maxMetricValue
    ? (
        globalMetric === "total_sales"
          ? Math.ceil(maxMetricValue / 20000) * 20000
          : maxMetricValue
      )
    : 100

  const chartTicks = [
    chartScaleMax,
    chartScaleMax * 0.75,
    chartScaleMax * 0.5,
    chartScaleMax * 0.25,
    0
  ]

  const getTrendRate = (
    currentValue,
    previousValue
  ) => {
    if (
      previousValue === null
      || previousValue === undefined
      || Number(previousValue) === 0
    ) {
      return null
    }

    return (
      (
        Number(currentValue)
        - Number(previousValue)
      )
      / Number(previousValue)
      * 100
    )
  }

  // 11A. 门店页面派生数据
  const storeRanking = storeData?.ranking || []
  const storeTrend = storeData?.trend || []
  const storeFilterOptions = storeData?.filters || {}
  const storePeriodLabel = (
    storeData?.period?.label || "最新周期"
  )
  const storeLatestDataDate = (
    storeData?.latest_data_date || "--"
  )

  const storeMetricOptions = [
    {
      value: "total_sales",
      label: "营业额",
      unit: "currency",
      digits: 0
    },
    {
      value: "order_count",
      label: "订单量",
      unit: "order",
      digits: 0
    },
    {
      value: "avg_order_value",
      label: "客单价",
      unit: "currency",
      digits: 2
    },
    {
      value: "total_quantity",
      label: "销量",
      unit: "quantity",
      digits: 0
    }
  ]

  const storeMetricConfig = (
    storeMetricOptions.find(
      (option) => option.value === storeMetric
    ) || storeMetricOptions[0]
  )

  const filteredStoreRanking = storeRanking.filter(
    (item) => (
      (!selectedStoreId
        || item.store_id === selectedStoreId)
      && (!selectedStoreCategory
        || item.category === selectedStoreCategory)
      && (!selectedStoreDistrict
        || item.district === selectedStoreDistrict)
    )
  )

  const sortedStoreRanking = [
    ...filteredStoreRanking
  ].sort((left, right) => (
    (Number(right[storeMetric]) || 0)
    - (Number(left[storeMetric]) || 0)
    || left.store_name.localeCompare(
      right.store_name,
      "zh-CN"
    )
  ))

  const selectedStoreIds = new Set(
    filteredStoreRanking.map(
      (item) => item.store_id
    )
  )
  const hasStoreSelectionFilters = Boolean(
    selectedStoreId
    || selectedStoreCategory
    || selectedStoreDistrict
  )

  const filteredStoreTrend = storeTrend.map(
    (period) => {
      if (!hasStoreSelectionFilters) {
        const totalSales = (
          Number(period.total_sales) || 0
        )
        const orderCount = (
          Number(period.order_count) || 0
        )

        return {
          ...period,
          total_sales: totalSales,
          order_count: orderCount,
          avg_order_value: orderCount
            ? totalSales / orderCount
            : 0,
          total_quantity: (
            Number(period.total_quantity) || 0
          )
        }
      }

      const matchingStores = (
        period.stores || []
      ).filter(
        (item) => selectedStoreIds.has(
          item.store_id
        )
      )
      const totalSales = matchingStores.reduce(
        (total, item) => (
          total + (Number(item.total_sales) || 0)
        ),
        0
      )
      const orderCount = matchingStores.reduce(
        (total, item) => (
          total + (Number(item.order_count) || 0)
        ),
        0
      )
      const totalQuantity = matchingStores.reduce(
        (total, item) => (
          total + (Number(item.total_quantity) || 0)
        ),
        0
      )

      return {
        ...period,
        total_sales: totalSales,
        order_count: orderCount,
        avg_order_value: orderCount
          ? totalSales / orderCount
          : 0,
        total_quantity: totalQuantity
      }
    }
  )

  const visibleStoreSales = filteredStoreRanking.reduce(
    (total, item) => (
      total + (Number(item.total_sales) || 0)
    ),
    0
  )
  const visibleStoreOrders = hasStoreSelectionFilters
    ? filteredStoreRanking.reduce(
        (total, item) => (
          total + (Number(item.order_count) || 0)
        ),
        0
      )
    : (Number(storeData?.summary?.order_count) || 0)
  const visibleStoreQuantity = filteredStoreRanking.reduce(
    (total, item) => (
      total + (Number(item.total_quantity) || 0)
    ),
    0
  )
  const visibleStoreAov = visibleStoreOrders
    ? visibleStoreSales / visibleStoreOrders
    : null
  const visibleTopStore = [
    ...filteredStoreRanking
  ].sort(
    (left, right) => (
      Number(right.total_sales)
      - Number(left.total_sales)
    )
  )[0] || null

  const storeChartMax = filteredStoreTrend.length
    ? Math.max(
        ...filteredStoreTrend.map(
          (item) => (
            Number(item[storeMetric]) || 0
          )
        )
      )
    : 0
  const storeChartScaleMax = storeChartMax || 100
  const storeChartTicks = [
    storeChartScaleMax,
    storeChartScaleMax * 0.75,
    storeChartScaleMax * 0.5,
    storeChartScaleMax * 0.25,
    0
  ]

  const formatStoreMetric = (value) => {
    const formattedValue = formatNumber(
      value,
      storeMetricConfig.digits
    )

    if (storeMetricConfig.unit === "currency") {
      return `¥${formattedValue}`
    }

    if (storeMetricConfig.unit === "order") {
      return `${formattedValue} 单`
    }

    return `${formattedValue} 件`
  }

  const hasActiveStoreFilters = Boolean(
    selectedStoreId
    || selectedStoreCategory
    || selectedStoreDistrict
    || storeMetric !== "total_sales"
  )

  const resetStoreFilters = () => {
    setSelectedStoreId("")
    setSelectedStoreCategory("")
    setSelectedStoreDistrict("")
    setStoreMetric("total_sales")
  }

  // 12. 页面结构
  return (
    <div
      className={`dashboard ${
        uiSettings.compact ? "compact-dashboard" : ""
      } ${
        uiSettings.animations ? "" : "no-animations"
      }`}
    >

      <aside className="sidebar">
        <div className="brand">
          M
        </div>

        <div className="sidebar-menu">
          <div
            className={`sidebar-item ${
              activePage === "home"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("home")
            }
          >
            <span className="sidebar-icon">⌂</span>
            <span>首页</span>
          </div>

          <div
            className={`sidebar-item ${
              activePage === "sales"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("sales")
            }
          >
            <span className="sidebar-icon">▣</span>
            <span>销售</span>
          </div>

          <div
            className={`sidebar-item ${
              activePage === "products" 
                  ? "active" 
                  : ""
            }`}
            onClick={() =>
                setActivePage("products")
          }
          >
            <span className="sidebar-icon">◫</span>
            <span>商品</span>
          </div>

          <div
            className={`sidebar-item ${
              activePage === "stores"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("stores")
            }
          >
            <span className="sidebar-icon">▤</span>
            <span>门店</span>
          </div>

          <div
            className={`sidebar-item ${
              activePage === "statistics"
                ? "active"
                : ""
            }`}
            onClick={() =>
              navigateToPage("statistics")
            }
          >
            <span className="sidebar-icon">◔</span>
            <span>统计</span>
          </div>

          <div
            className={`sidebar-item ${
              activePage === "tools"
                ? "active"
                : ""
            }`}
            onClick={() =>
              navigateToPage("tools")
            }
          >
            <span className="sidebar-icon">⌁</span>
            <span>工具</span>
          </div>
        </div>

        <button
          type="button"
          className="sidebar-bottom"
          aria-label="界面设置"
          onClick={() => setSettingsOpen(true)}
        >
          ⚙
        </button>
      </aside>


      <main className="main-area">

        <header className="topbar">
          <div className="topbar-left">
            <div
              className={`top-tab ${
                activePage === "home"
                  ? "active"
                  : ""
              }`}
              onClick={() =>
                setActivePage("home")
              }
            >
              首页
            </div>

            <div
              className={`top-tab ${
                activePage === "reports" ? "active" : ""
              }`}
              onClick={() => navigateToPage("reports")}
            >
              我的报表
            </div>

            <div
              className={`top-tab ${
                activePage === "analysis" ? "active" : ""
              }`}
              onClick={() => navigateToPage("analysis")}
            >
              经营分析
            </div>

            <div
              className={`top-tab ${
                activePage === "data-center" ? "active" : ""
              }`}
              onClick={() => navigateToPage("data-center")}
            >
              数据中心
            </div>
          </div>

          <div className="topbar-right">
            <button
              className="ai-button"
              onClick={() =>
                setAiOpen(true)
              }
            >
              AI助手
            </button>

            <button
              type="button"
              className="topbar-text-button"
              onClick={() => setHelpOpen(true)}
            >
              帮助
            </button>

            <div className="topbar-popover-anchor">
              <button
                type="button"
                className="notification-button"
                aria-label="通知"
                onClick={() => {
                  setNotificationsOpen((current) => !current)
                  setProfileOpen(false)
                }}
              >
                ◉
                <span className="notification-badge"></span>
              </button>
              <NotificationsPanel
                open={notificationsOpen}
                latestDataDate={latestDataDate}
                onClose={() => setNotificationsOpen(false)}
              />
            </div>

            <div className="topbar-popover-anchor">
              <button
                type="button"
                className="profile-trigger"
                onClick={() => {
                  setProfileOpen((current) => !current)
                  setNotificationsOpen(false)
                }}
              >
                <span className="avatar">M</span>
                <span className="admin-name">管理员</span>
              </button>
              <ProfileMenu
                open={profileOpen}
                onSettings={openSettings}
                onNewSession={() => {
                  handleNewSession()
                  setProfileOpen(false)
                }}
                onClose={() => setProfileOpen(false)}
              />
            </div>
          </div>
        </header>


        {activePage === "stores" ? (
          <div className="filter-bar store-filter-bar">
            <label className="store-filter-control">
              <span>门店</span>
              <select
                value={selectedStoreId}
                onChange={(event) =>
                  setSelectedStoreId(event.target.value)
                }
                disabled={storeLoading}
              >
                <option value="">全部门店</option>
                {(storeFilterOptions.stores || []).map(
                  (store) => (
                    <option
                      value={store.store_id}
                      key={store.store_id}
                    >
                      {store.store_name}
                    </option>
                  )
                )}
              </select>
            </label>

            <label className="store-filter-control">
              <span>品类</span>
              <select
                value={selectedStoreCategory}
                onChange={(event) =>
                  setSelectedStoreCategory(event.target.value)
                }
                disabled={storeLoading}
              >
                <option value="">全部品类</option>
                {(storeFilterOptions.categories || []).map(
                  (category) => (
                    <option value={category} key={category}>
                      {category}
                    </option>
                  )
                )}
              </select>
            </label>

            <label className="store-filter-control">
              <span>区域</span>
              <select
                value={selectedStoreDistrict}
                onChange={(event) =>
                  setSelectedStoreDistrict(event.target.value)
                }
                disabled={storeLoading}
              >
                <option value="">全部区域</option>
                {(storeFilterOptions.districts || []).map(
                  (district) => (
                    <option value={district} key={district}>
                      {district}
                    </option>
                  )
                )}
              </select>
            </label>

            <label className="store-filter-control">
              <span>指标</span>
              <select
                value={storeMetric}
                onChange={(event) =>
                  setStoreMetric(event.target.value)
                }
                disabled={storeLoading}
              >
                {storeMetricOptions.map(
                  (option) => (
                    <option
                      value={option.value}
                      key={option.value}
                    >
                      {option.label}
                    </option>
                  )
                )}
              </select>
            </label>

            <button
              type="button"
              className="store-filter-reset"
              onClick={resetStoreFilters}
              disabled={!hasActiveStoreFilters}
            >
              重置
            </button>

            <div className="filter-divider"></div>

            <span className="filter-tip">
              {storeLoading
                ? "正在加载门店筛选项"
                : storeError
                  || `显示 ${filteredStoreRanking.length} / ${storeRanking.length} 家门店`}
            </span>
          </div>
        ) : (
          <GlobalFilterBar
            filters={analyticsData?.filters || {}}
            values={globalFilterValues}
            metricOptions={dashboardMetricOptions}
            loading={analyticsLoading}
            error={analyticsError}
            resultCount={analyticsData?.product_ranking?.length || 0}
            onChange={handleGlobalFilterChange}
            onReset={resetGlobalFilters}
          />
        )}


        <div className="workspace">
          {activePage === "home" ? (
            <>

          <section className="panel overview-panel">
            <div className="panel-header">
              <div>
                <h2>
                  经营概览
                </h2>

                <span>
                  {dashboardLoading
                    ? "正在加载真实经营数据"
                    : dashboardError
                      || `基于 ${periodLabel} 真实经营数据`}
                </span>
              </div>

              <TimeScopeTabs
                value={timeScope}
                onChange={setTimeScope}
              />
            </div>


            <div className="metric-grid">

              <div className="metric-item">
                <span className="metric-name">
                  营业额
                </span>

                <strong>
                  ¥{formatNumber(
                    summary.total_sales
                  )}
                </strong>

                <small>
                  {periodLabel}总营业额
                </small>
              </div>

              <div className="metric-item">
                <span className="metric-name">
                  订单量
                </span>

                <strong>
                  {formatNumber(
                    summary.order_count
                  )} 单
                </strong>

                <small>
                  {periodLabel}去重订单数
                </small>
              </div>

              <div className="metric-item">
                <span className="metric-name">
                  客单价
                </span>

                <strong>
                  ¥{formatNumber(
                    summary.avg_order_value,
                    2
                  )}
                </strong>

                <small>
                  平均每单销售额
                </small>
              </div>

              <div className="metric-item">
                <span className="metric-name">
                  领先品类
                </span>

                <strong>
                  {summary.top_category || "--"}
                </strong>

                <small>
                  {summary.top_category
                    ? `${periodLabel}营业额 ¥${formatNumber(
                        summary.top_category_sales
                      )}`
                    : "暂无品类数据"}
                </small>
              </div>

              <div className="metric-item">
                <span className="metric-name">
                  数据来源
                </span>

                <strong>
                  SQLite
                </strong>

                <small>
                  更新至 {latestDataDate}
                </small>
              </div>

            </div>
          </section>


          <section className="panel trend-panel">

            <div className="panel-header">
              <div>
                <h2>
                  经营趋势
                </h2>

                <span>
                  最近三个月真实经营指标
                </span>
              </div>

              <TimeScopeTabs
                value={timeScope}
                onChange={setTimeScope}
              />
            </div>


            <div className="trend-summary">

              <div className="trend-card">
                <span>
                  销售额
                </span>

                <strong>
                  ¥{formatNumber(
                    summary.total_sales
                  )}
                </strong>

                <small>
                  {formatRate(
                    summary.sales_change_rate
                  )}
                </small>
              </div>

              <div className="trend-card">
                <span>
                  订单量
                </span>

                <strong>
                  {formatNumber(
                    summary.order_count
                  )} 单
                </strong>

                <small>
                  {formatRate(
                    summary.order_change_rate
                  )}
                </small>
              </div>

              <div className="trend-card">
                <span>
                  客单价
                </span>

                <strong>
                  ¥{formatNumber(
                    summary.avg_order_value,
                    2
                  )}
                </strong>

                <small>
                  {formatRate(
                    summary.aov_change_rate
                  )}
                </small>
              </div>

              <div className="trend-card">
                <span>
                  门店品类
                </span>

                <strong>
                  {summary.top_category || "--"}
                </strong>

                <small>
                  {summary.top_category
                    ? `${periodLabel}营业额 ¥${formatNumber(
                        summary.top_category_sales
                      )}`
                    : "暂无品类数据"}
                </small>
              </div>

            </div>


            <div className="chart-area">

              <div className="chart-y-axis">
                {chartTicks.map(
                  (tick, index) => (
                    <span key={index}>
                      {formatNumber(
                        Math.round(tick)
                      )}
                    </span>
                  )
                )}
              </div>

              <div className="chart-content">

                <div className="grid-line"></div>
                <div className="grid-line"></div>
                <div className="grid-line"></div>
                <div className="grid-line"></div>
                <div className="grid-line"></div>

                {trend.length ? (
                  <div className="sales-bar-chart">
                    {trend.map((item) => {
                      const barHeight = chartScaleMax
                        ? (
                            Number(
                              item[globalMetric]
                            )
                            / chartScaleMax
                            * 100
                          )
                        : 0

                      return (
                        <div
                          className="sales-bar-column"
                          key={item.month}
                        >
                          <div className="sales-bar-value">
                            {formatDashboardMetric(item[globalMetric])}
                          </div>

                          <div className="sales-bar-track">
                            <div
                              className="sales-bar-fill"
                              style={{
                                height: `${barHeight}%`
                              }}
                            ></div>
                          </div>

                          <div className="sales-bar-label">
                            {item.label}
                          </div>
                        </div>
                      )
                    })}
                  </div>
                ) : (
                  <div className="chart-empty">
                    {dashboardLoading
                      ? "正在加载真实趋势数据..."
                      : dashboardError
                        || "暂无趋势数据"}
                  </div>
                )}

              </div>

            </div>

          </section>


          <section className="panel table-panel">

            <div className="panel-header">
              <div>
                <h2>
                  业务分析
                </h2>

                <span>
                  {trend.length
                    ? `真实数据范围：${trend[0].label} - ${trend[trend.length - 1].label}`
                    : "当前已支持的数据分析类型"}
                </span>
              </div>
            </div>


            <div className="table-tabs">
              {[
                ["products", "商品"],
                ["stores", "门店"],
                ["categories", "品类"],
                ["aov", "客单价"]
              ].map(([key, label]) => (
                <button
                  type="button"
                  className={
                    businessAnalysisTab === key
                      ? "selected"
                      : ""
                  }
                  onClick={() => setBusinessAnalysisTab(key)}
                  key={key}
                >
                  {label}
                </button>
              ))}
            </div>


            <table>
              <thead>
                <tr>
                  <th>
                    分析类型
                  </th>

                  <th>
                    查询能力
                  </th>

                  <th>
                    时间范围
                  </th>

                  <th>
                    数据来源
                  </th>

                  <th>
                    状态
                  </th>
                </tr>
              </thead>

              <tbody>
                {visibleBusinessCapabilities.map((item) => (
                  <tr key={item.tab}>
                    <td>{item.type}</td>
                    <td>{item.capability}</td>
                    <td>{item.range}</td>
                    <td>SQLite</td>
                    <td>
                      <span className="status-tag">
                        可用
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

          </section>
            </>
          ) : activePage === "sales" ? (
          <>
          <section className="panel sales-page-header">
            <div className="panel-header">
              <div>
                <h2>
                  销售分析
                </h2>

                <span>
                  {dashboardLoading
                    ? "正在加载真实销售数据"
                    : dashboardError
                      || `基于 ${periodLabel} SQLite 经营数据`}
                </span>
              </div>

              <TimeScopeTabs
                value={timeScope}
                onChange={setTimeScope}
              />
            </div>

            <div className="sales-kpi-grid">
              <div className="sales-kpi-card">
                <span>
                  {timeScope === 1 ? "月营业额" : "近3月营业额"}
                </span>

                <strong>
                  ¥{formatNumber(
                    summary.total_sales
                  )}
                </strong>

                <small>
                  {formatRate(
                    summary.sales_change_rate
                  )}
                </small>
              </div>

              <div className="sales-kpi-card">
                <span>
                  {timeScope === 1 ? "月订单量" : "近3月订单量"}
                </span>

                <strong>
                  {formatNumber(
                    summary.order_count
                  )} 单
                </strong>

                <small>
                  {formatRate(
                    summary.order_change_rate
                  )}
                </small>
              </div>

              <div className="sales-kpi-card">
                <span>
                  客单价
                </span>

                <strong>
                  ¥{formatNumber(
                    summary.avg_order_value,
                    2
                  )}
                </strong>

                <small>
                  {formatRate(
                    summary.aov_change_rate
                  )}
                </small>
              </div>

              <div className="sales-kpi-card">
                <span>
                  当前周期
                </span>

                <strong>
                  {periodLabel}
                </strong>

                <small>
                  数据截止 {latestDataDate}
                </small>
              </div>
            </div>
          </section>


          <section className="panel sales-trend-panel">
            <div className="panel-header">
              <div>
                <h2>
                  月度{dashboardMetricConfig.label}趋势
                </h2>

                <span>
                  最近三个月真实销售额
                </span>
              </div>
            </div>

            <div className="chart-area sales-page-chart">
              <div className="chart-y-axis">
                {chartTicks.map(
                  (tick, index) => (
                    <span key={index}>
                      {formatNumber(
                        Math.round(tick)
                      )}
                    </span>
                  )
                )}
              </div>

              <div className="chart-content">
                <div className="grid-line"></div>
                <div className="grid-line"></div>
                <div className="grid-line"></div>
                <div className="grid-line"></div>
                <div className="grid-line"></div>

                {trend.length ? (
                  <div className="sales-bar-chart">
                    {trend.map((item) => {
                      const barHeight = chartScaleMax
                        ? (
                            Number(
                              item[globalMetric]
                            )
                            / chartScaleMax
                            * 100
                          )
                        : 0

                      return (
                        <div
                          className="sales-bar-column"
                          key={item.month}
                        >
                          <div className="sales-bar-value">
                            {formatDashboardMetric(item[globalMetric])}
                          </div>

                          <div className="sales-bar-track">
                            <div
                              className="sales-bar-fill"
                              style={{
                                height: `${barHeight}%`
                              }}
                            ></div>
                          </div>

                          <div className="sales-bar-label">
                            {item.label}
                          </div>
                        </div>
                      )
                    })}
                  </div>
                ) : (
                  <div className="chart-empty">
                    {dashboardLoading
                      ? "正在加载真实销售趋势..."
                      : dashboardError
                        || "暂无销售趋势数据"}
                  </div>
                )}
              </div>
            </div>
          </section>


          <section className="panel sales-detail-panel">
            <div className="panel-header">
              <div>
                <h2>
                  月度销售明细
                </h2>

                <span>
                  数据直接来源于 SQLite 销售表
                </span>
              </div>
            </div>

            <table>
              <thead>
                <tr>
                  <th>月份</th>
                  <th>营业额</th>
                  <th>订单量</th>
                  <th>客单价</th>
                  <th>营业额环比</th>
                </tr>
              </thead>

              <tbody>
                {trend.map(
                  (item, index) => {
                    const previous = (
                      index > 0
                        ? trend[index - 1]
                        : null
                    )

                    const rate = previous
                      ? getTrendRate(
                          item.total_sales,
                          previous.total_sales
                        )
                      : null

                    return (
                      <tr key={item.month}>
                        <td>
                          {item.month}
                        </td>

                        <td>
                          ¥{formatNumber(
                            item.total_sales
                          )}
                        </td>

                        <td>
                          {formatNumber(
                            item.order_count
                          )} 单
                        </td>

                        <td>
                          ¥{formatNumber(
                            item.avg_order_value,
                            2
                          )}
                        </td>

                        <td>
                          {rate === null
                            ? "--"
                            : `${rate > 0 ? "+" : ""}${rate.toFixed(2)}%`}
                        </td>
                      </tr>
                    )
                  }
                )}
              </tbody>
            </table>
            </section>
</>

) : activePage === "products" ? (

<>
<section className="panel product-page">

<div className="panel-header">

<div>

<h2>
商品分析
</h2>

<span>
{
analyticsLoading
?
"正在加载商品数据"
:
analyticsError
||
"基于 SQLite 商品销售数据"
}
</span>

</div>


<TimeScopeTabs
value={timeScope}
onChange={setTimeScope}
/>

</div>



<div className="sales-kpi-grid">


<div className="sales-kpi-card">

<span>
商品数量
</span>

<strong>
{
productSummary.total_products || "--"
}
</strong>

<small>
当前商品池
</small>

</div>



<div className="sales-kpi-card">

<span>
商品销售额
</span>

<strong>
¥{
formatNumber(
productSummary.total_sales
)
}
</strong>

<small>
当前周期
</small>

</div>



<div className="sales-kpi-card">

<span>
销售数量
</span>

<strong>
{
formatNumber(
productSummary.total_quantity
)
}
</strong>

<small>
商品销量
</small>

</div>



<div className="sales-kpi-card">

<span>
TOP商品
</span>

<strong>
{
productSummary.top_product || "--"
}
</strong>

<small>
¥{
formatNumber(
productSummary.top_product_sales
)
}
</small>

</div>


</div>


</section>



<section className="panel">


<div className="panel-header">

<h2>
商品销售排行
</h2>

<span>
按{dashboardMetricConfig.label}从高到低排列
</span>

</div>



<table>

<thead>

<tr>

<th>
排名
</th>

<th>
商品
</th>

<th>
销售额
</th>

<th>
销量
</th>

<th>
订单量
</th>

<th>
客单价
</th>

</tr>

</thead>



<tbody>

{
productRanking.map(
(item,index)=>(
<tr key={item.product_name}>

<td>
{index+1}
</td>

<td>
{item.product_name}
</td>

<td>
¥{
formatNumber(
item.total_sales
)
}
</td>

<td>
{
formatNumber(
item.total_quantity
)
}
</td>

<td>
{
formatNumber(
item.order_count
)
} 单
</td>

<td>
¥{
formatNumber(
item.avg_order_value,
2
)
}
</td>

</tr>
)
)
}


</tbody>


</table>



</section>

</>

) : activePage === "stores" ? (
<>
  <section className="panel store-overview-panel">
    <div className="panel-header">
      <div>
        <h2>
          门店经营
        </h2>

        <span>
          {storeLoading
            ? "正在加载真实门店数据"
            : storeError
              || `基于 ${storePeriodLabel} SQLite 门店数据，共 ${formatNumber(storeData?.summary?.total_stores)} 家门店`}
        </span>
      </div>

      <div className="period-tabs">
        <span className="selected">
          最新月
        </span>

        <span>
          更新至 {storeLatestDataDate}
        </span>
      </div>
    </div>

    <div className="store-kpi-grid">
      <div className="sales-kpi-card">
        <span>
          筛选门店
        </span>

        <strong>
          {formatNumber(
            filteredStoreRanking.length
          )} 家
        </strong>

        <small>
          {formatNumber(
            filteredStoreRanking.filter(
              (item) => item.order_count > 0
            ).length
          )} 家有交易
        </small>
      </div>

      <div className="sales-kpi-card">
        <span>
          门店营业额
        </span>

        <strong>
          ¥{formatNumber(
            visibleStoreSales
          )}
        </strong>

        <small>
          {storePeriodLabel}筛选汇总
        </small>
      </div>

      <div className="sales-kpi-card">
        <span>
          门店订单量
        </span>

        <strong>
          {formatNumber(
            visibleStoreOrders
          )} 单
        </strong>

        <small>
          销量 {formatNumber(
            visibleStoreQuantity
          )} 件
        </small>
      </div>

      <div className="sales-kpi-card">
        <span>
          综合客单价
        </span>

        <strong>
          ¥{formatNumber(
            visibleStoreAov,
            2
          )}
        </strong>

        <small>
          按筛选范围营业额 / 订单量
        </small>
      </div>

      <div className="sales-kpi-card">
        <span>
          营业额领先门店
        </span>

        <strong>
          {visibleTopStore?.store_name || "--"}
        </strong>

        <small>
          {visibleTopStore
            ? `¥${formatNumber(visibleTopStore.total_sales)}`
            : "当前筛选暂无数据"}
        </small>
      </div>
    </div>
  </section>

  <section className="panel store-trend-panel">
    <div className="panel-header store-panel-header">
      <div>
        <h2>
          门店{storeMetricConfig.label}趋势
        </h2>

        <span>
          最近三个月，跟随当前门店筛选实时汇总
        </span>
      </div>

      <div
        className="store-metric-tabs"
        aria-label="门店趋势指标"
      >
        {storeMetricOptions.map(
          (option) => (
            <button
              type="button"
              className={
                storeMetric === option.value
                  ? "selected"
                  : ""
              }
              onClick={() =>
                setStoreMetric(option.value)
              }
              key={option.value}
            >
              {option.label}
            </button>
          )
        )}
      </div>
    </div>

    <div className="chart-area store-trend-chart">
      <div className="chart-y-axis store-chart-y-axis">
        {storeChartTicks.map(
          (tick, index) => (
            <span key={index}>
              {formatStoreMetric(tick)}
            </span>
          )
        )}
      </div>

      <div className="chart-content">
        <div className="grid-line"></div>
        <div className="grid-line"></div>
        <div className="grid-line"></div>
        <div className="grid-line"></div>
        <div className="grid-line"></div>

        {filteredStoreTrend.length
          && selectedStoreIds.size ? (
          <div className="sales-bar-chart store-bar-chart">
            {filteredStoreTrend.map((item) => {
              const metricValue = (
                Number(item[storeMetric]) || 0
              )
              const barHeight = (
                metricValue
                / storeChartScaleMax
                * 100
              )

              return (
                <div
                  className="sales-bar-column"
                  key={item.month}
                >
                  <div className="sales-bar-value">
                    {formatStoreMetric(metricValue)}
                  </div>

                  <div className="sales-bar-track">
                    <div
                      className="sales-bar-fill"
                      style={{
                        height: `${barHeight}%`
                      }}
                    ></div>
                  </div>

                  <div className="sales-bar-label">
                    {item.label}
                  </div>
                </div>
              )
            })}
          </div>
        ) : (
          <div className="chart-empty">
            {storeLoading
              ? "正在加载门店趋势..."
              : storeError
                || "当前筛选暂无趋势数据"}
          </div>
        )}
      </div>
    </div>
  </section>

  <section className="panel store-ranking-panel">
    <div className="panel-header">
      <div>
        <h2>
          门店经营排行
        </h2>

        <span>
          按{storeMetricConfig.label}从高到低排列，销售占比基于全部门店
        </span>
      </div>

      <span className="store-result-count">
        {sortedStoreRanking.length} 条结果
      </span>
    </div>

    <div className="store-table-scroll">
      <table>
        <thead>
          <tr>
            <th>排名</th>
            <th>门店</th>
            <th>品类</th>
            <th>区域</th>
            <th>营业额</th>
            <th>订单量</th>
            <th>客单价</th>
            <th>销量</th>
            <th>销售占比</th>
          </tr>
        </thead>

        <tbody>
          {sortedStoreRanking.length ? (
            sortedStoreRanking.map(
              (item, index) => (
                <tr key={item.store_id}>
                  <td>
                    <span
                      className={`store-rank-badge ${
                        index < 3 ? "leading" : ""
                      }`}
                    >
                      {index + 1}
                    </span>
                  </td>

                  <td>
                    <strong className="store-name">
                      {item.store_name}
                    </strong>

                    <small className="store-code">
                      {item.store_id}
                    </small>
                  </td>

                  <td>
                    {item.category}
                  </td>

                  <td>
                    {item.district}
                  </td>

                  <td>
                    ¥{formatNumber(
                      item.total_sales
                    )}
                  </td>

                  <td>
                    {formatNumber(
                      item.order_count
                    )} 单
                  </td>

                  <td>
                    ¥{formatNumber(
                      item.avg_order_value,
                      2
                    )}
                  </td>

                  <td>
                    {formatNumber(
                      item.total_quantity
                    )} 件
                  </td>

                  <td>
                    {formatNumber(
                      item.sales_share,
                      2
                    )}%
                  </td>
                </tr>
              )
            )
          ) : (
            <tr>
              <td
                className="store-table-empty"
                colSpan="9"
              >
                {storeLoading
                  ? "正在加载门店排行..."
                  : storeError
                    || "当前筛选条件下暂无门店数据"}
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  </section>
</>
) : activePage === "reports" ? (
  <ReportsPage
    analytics={analyticsData}
    formatNumber={formatNumber}
  />
) : activePage === "analysis" ? (
  <AnalysisPage
    analytics={analyticsData}
    formatNumber={formatNumber}
    onOpenAI={() => setAiOpen(true)}
    onRefresh={refreshAnalytics}
  />
) : activePage === "statistics" ? (
  <StatisticsPage
    analytics={analyticsData}
    formatNumber={formatNumber}
  />
) : activePage === "tools" ? (
  <ToolsPage
    onOpenAI={() => setAiOpen(true)}
    onRefresh={refreshAnalytics}
    formatNumber={formatNumber}
  />
) : activePage === "data-center" ? (
  <DataCenterPage
    analytics={analyticsData}
    loading={analyticsLoading}
    error={analyticsError}
    onRefresh={refreshAnalytics}
    formatNumber={formatNumber}
  />
) : null}
        </div>
      </main>

      <HelpPanel
        open={helpOpen}
        onClose={() => setHelpOpen(false)}
      />

      <SettingsDrawer
        open={settingsOpen}
        settings={uiSettings}
        onChange={handleUiSettingChange}
        onClose={() => setSettingsOpen(false)}
      />


      {aiOpen && (
        <div
          className="drawer-mask"
          onClick={() =>
            setAiOpen(false)
          }
        ></div>
      )}


      <aside
        className={`ai-drawer ${aiOpen ? "open" : ""}`}
      >

        <div className="drawer-header">

          <div>
            <h3>
              AI 经营分析助手
            </h3>

            <span>
              基于经营数据库智能分析
            </span>
          </div>

          <div className="drawer-header-actions">
            <button
              type="button"
              className="new-session-button"
              onClick={handleNewSession}
              disabled={loading}
            >
              新会话
            </button>

            <button
              type="button"
              className="close-button"
              onClick={() =>
                setAiOpen(false)
              }
            >
              ×
            </button>
          </div>

        </div>


        <div className="drawer-tools">

          <div className="drawer-tool-title">
            数据分析
          </div>

          <div className="drawer-tool-desc">
            查询商品销售、门店品类和客单价趋势
          </div>

        </div>


        <div className="chat-area">

          {messages.map((message, index) => (
            <div
              key={index}
              className={`message-row ${message.role}`}
            >

              <div className="message-avatar">
                {message.role === "assistant"
                  ? "AI"
                  : "我"}
              </div>

              <div
                className={`message-bubble ${message.role}`}
              >
                {message.content}
              </div>

            </div>
          ))}


          {loading && (
            <div className="message-row assistant">

              <div className="message-avatar">
                AI
              </div>

              <div className="message-bubble assistant">
                正在分析经营数据...
              </div>

            </div>
          )}

        </div>


        <form
          className="drawer-input"
          onSubmit={handleSubmit}
        >

          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(
                event.target.value
              )
            }
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault()
                event.currentTarget.form?.requestSubmit()
              }
            }}
            placeholder="输入经营分析问题..."
            disabled={loading}
          />

          <div className="drawer-input-bottom">

            <span>
              Enter 发送 · Shift+Enter 换行
            </span>

            <button
              type="submit"
              disabled={loading}
            >
              ↑
            </button>

          </div>

        </form>

      </aside>

    </div>
  )
}


export default App