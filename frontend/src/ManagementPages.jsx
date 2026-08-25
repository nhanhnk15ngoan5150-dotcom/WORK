import { useState } from "react"


const downloadTextFile = (
  filename,
  content,
  type = "text/plain;charset=utf-8"
) => {
  const blob = new Blob(
    [content],
    { type }
  )
  const url = URL.createObjectURL(blob)
  const link = document.createElement("a")

  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(url)
}


export function GlobalFilterBar({
  filters,
  values,
  metricOptions,
  loading,
  error,
  resultCount,
  onChange,
  onReset
}) {
  const hasFilters = Boolean(
    values.storeId
    || values.category
    || values.productId
    || values.metric !== "total_sales"
  )

  return (
    <div className="filter-bar global-filter-bar">
      <label className="global-filter-control">
        <span>门店</span>
        <select
          value={values.storeId}
          onChange={(event) =>
            onChange("storeId", event.target.value)
          }
          disabled={loading}
        >
          <option value="">全部门店</option>
          {(filters.stores || []).map((store) => (
            <option
              value={store.store_id}
              key={store.store_id}
            >
              {store.store_name}
            </option>
          ))}
        </select>
      </label>

      <label className="global-filter-control">
        <span>品类</span>
        <select
          value={values.category}
          onChange={(event) =>
            onChange("category", event.target.value)
          }
          disabled={loading}
        >
          <option value="">全部品类</option>
          {(filters.categories || []).map((category) => (
            <option value={category} key={category}>
              {category}
            </option>
          ))}
        </select>
      </label>

      <label className="global-filter-control">
        <span>商品</span>
        <select
          value={values.productId}
          onChange={(event) =>
            onChange("productId", event.target.value)
          }
          disabled={loading}
        >
          <option value="">全部商品</option>
          {(filters.products || []).map((product) => (
            <option
              value={product.product_id}
              key={product.product_id}
            >
              {product.product_name}
            </option>
          ))}
        </select>
      </label>

      <label className="global-filter-control">
        <span>指标</span>
        <select
          value={values.metric}
          onChange={(event) =>
            onChange("metric", event.target.value)
          }
          disabled={loading}
        >
          {metricOptions.map((option) => (
            <option value={option.value} key={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </label>

      <button
        type="button"
        className="global-filter-reset"
        onClick={onReset}
        disabled={!hasFilters}
      >
        重置
      </button>

      <div className="filter-divider"></div>

      <span className="filter-tip">
        {loading
          ? "正在应用经营筛选"
          : error
            || `筛选结果 ${resultCount} 条`}
      </span>
    </div>
  )
}


export function TimeScopeTabs({
  value,
  onChange
}) {
  return (
    <div
      className="period-tabs interactive-period-tabs"
      aria-label="经营时间范围"
    >
      <button
        type="button"
        className={value === 1 ? "selected" : ""}
        onClick={() => onChange(1)}
      >
        最新月
      </button>
      <button
        type="button"
        className={value === 3 ? "selected" : ""}
        onClick={() => onChange(3)}
      >
        近3月
      </button>
    </div>
  )
}


export function ReportsPage({
  analytics,
  formatNumber
}) {
  const [reportType, setReportType] = useState("products")
  const definitions = {
    products: {
      label: "商品经营报表",
      rows: analytics?.product_ranking || [],
      columns: [
        ["排名", "rank"],
        ["商品", "product_name"],
        ["营业额", "total_sales"],
        ["订单量", "order_count"],
        ["销量", "total_quantity"],
      ],
    },
    stores: {
      label: "门店经营报表",
      rows: analytics?.store_ranking || [],
      columns: [
        ["排名", "rank"],
        ["门店", "store_name"],
        ["品类", "category"],
        ["营业额", "total_sales"],
        ["订单量", "order_count"],
      ],
    },
    categories: {
      label: "品类经营报表",
      rows: analytics?.category_ranking || [],
      columns: [
        ["排名", "rank"],
        ["品类", "category"],
        ["营业额", "total_sales"],
        ["订单量", "order_count"],
        ["销售占比", "sales_share"],
      ],
    },
    monthly: {
      label: "月度趋势报表",
      rows: analytics?.trend || [],
      columns: [
        ["月份", "month"],
        ["营业额", "total_sales"],
        ["订单量", "order_count"],
        ["客单价", "avg_order_value"],
        ["销量", "total_quantity"],
      ],
    },
  }
  const current = definitions[reportType]

  const displayCell = (key, value) => {
    if (key === "total_sales" || key === "avg_order_value") {
      return `¥${formatNumber(value, key === "avg_order_value" ? 2 : 0)}`
    }

    if (key === "sales_share") {
      return `${formatNumber(value, 2)}%`
    }

    return value ?? "--"
  }

  const exportCsv = () => {
    const header = current.columns.map(([label]) => label)
    const body = current.rows.map((row) => (
      current.columns.map(([, key]) => (
        `"${String(row[key] ?? "").replaceAll('"', '""')}"`
      )).join(",")
    ))
    const csv = [
      header.join(","),
      ...body,
    ].join("\n")

    downloadTextFile(
      `${current.label}.csv`,
      `\ufeff${csv}`,
      "text/csv;charset=utf-8"
    )
  }

  return (
    <>
      <section className="panel management-hero">
        <div>
          <span className="management-eyebrow">REPORTS</span>
          <h2>我的报表</h2>
          <p>根据当前全局筛选即时生成，可导出 CSV 或调用浏览器打印。</p>
        </div>
        <div className="management-actions">
          <button type="button" onClick={exportCsv}>
            导出 CSV
          </button>
          <button type="button" onClick={() => window.print()}>
            打印报表
          </button>
        </div>
      </section>

      <section className="panel management-panel">
        <div className="management-tabs">
          {Object.entries(definitions).map(([key, definition]) => (
            <button
              type="button"
              className={reportType === key ? "selected" : ""}
              onClick={() => setReportType(key)}
              key={key}
            >
              {definition.label}
            </button>
          ))}
        </div>

        <div className="management-table-scroll">
          <table>
            <thead>
              <tr>
                {current.columns.map(([label]) => (
                  <th key={label}>{label}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {current.rows.length ? current.rows.map((row, index) => (
                <tr key={row.product_id || row.store_id || row.category || row.month || index}>
                  {current.columns.map(([, key]) => (
                    <td key={key}>{displayCell(key, row[key])}</td>
                  ))}
                </tr>
              )) : (
                <tr>
                  <td colSpan={current.columns.length} className="management-empty">
                    当前筛选暂无可导出的报表数据
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </>
  )
}


export function AnalysisPage({
  analytics,
  formatNumber,
  onOpenAI,
  onRefresh
}) {
  const summary = analytics?.summary || {}
  const trend = analytics?.trend || []
  const first = trend[0]
  const latest = trend[trend.length - 1]
  const salesGrowth = first?.total_sales
    ? (
        (Number(latest?.total_sales || 0) - Number(first.total_sales))
        / Number(first.total_sales)
        * 100
      )
    : null

  const insights = [
    {
      title: "收入表现",
      value: `¥${formatNumber(summary.total_sales)}`,
      detail: salesGrowth === null
        ? "暂无完整趋势基线"
        : `近三个月变化 ${salesGrowth > 0 ? "+" : ""}${salesGrowth.toFixed(2)}%`,
    },
    {
      title: "订单效率",
      value: `${formatNumber(summary.order_count)} 单`,
      detail: `综合客单价 ¥${formatNumber(summary.avg_order_value, 2)}`,
    },
    {
      title: "领先门店",
      value: summary.top_store?.store_name || "--",
      detail: summary.top_store
        ? `贡献 ¥${formatNumber(summary.top_store.total_sales)}`
        : "暂无门店数据",
    },
    {
      title: "领先商品",
      value: summary.top_product?.product_name || "--",
      detail: summary.top_product
        ? `贡献 ¥${formatNumber(summary.top_product.total_sales)}`
        : "暂无商品数据",
    },
  ]

  return (
    <>
      <section className="panel management-hero analysis-hero">
        <div>
          <span className="management-eyebrow">ANALYSIS</span>
          <h2>经营分析</h2>
          <p>把当前筛选后的经营数据整理为可行动的关键结论。</p>
        </div>
        <div className="management-actions">
          <button type="button" onClick={onRefresh}>刷新分析</button>
          <button type="button" className="primary" onClick={onOpenAI}>
            继续问 AI
          </button>
        </div>
      </section>

      <section className="analysis-insight-grid">
        {insights.map((insight) => (
          <article className="panel analysis-insight-card" key={insight.title}>
            <span>{insight.title}</span>
            <strong>{insight.value}</strong>
            <small>{insight.detail}</small>
          </article>
        ))}
      </section>

      <section className="panel management-panel">
        <div className="panel-header">
          <div>
            <h2>建议关注</h2>
            <span>根据当前筛选结果自动生成</span>
          </div>
        </div>
        <div className="recommendation-list">
          <div>
            <strong>优先复核低贡献门店</strong>
            <span>{analytics?.store_ranking?.at(-1)?.store_name || "暂无门店"} 当前位于营业额末位。</span>
          </div>
          <div>
            <strong>跟进领先品类供给</strong>
            <span>{summary.top_category?.category || "暂无品类"} 当前贡献最高，建议核对库存和高峰排班。</span>
          </div>
          <div>
            <strong>结合趋势安排目标</strong>
            <span>最近周期营业额为 ¥{formatNumber(latest?.total_sales)}，目标应以真实趋势为基线。</span>
          </div>
        </div>
      </section>
    </>
  )
}


export function StatisticsPage({
  analytics,
  formatNumber
}) {
  const [dimension, setDimension] = useState("stores")
  const dimensions = {
    stores: {
      label: "门店分布",
      rows: analytics?.store_ranking || [],
      nameKey: "store_name",
    },
    products: {
      label: "商品分布",
      rows: analytics?.product_ranking || [],
      nameKey: "product_name",
    },
    categories: {
      label: "品类分布",
      rows: analytics?.category_ranking || [],
      nameKey: "category",
    },
  }
  const current = dimensions[dimension]
  const maxSales = Math.max(
    ...current.rows.map((item) => Number(item.total_sales) || 0),
    1
  )

  return (
    <>
      <section className="panel management-hero">
        <div>
          <span className="management-eyebrow">STATISTICS</span>
          <h2>统计</h2>
          <p>从门店、商品和品类三个维度查看当前筛选的贡献结构。</p>
        </div>
      </section>

      <section className="panel management-panel">
        <div className="management-tabs">
          {Object.entries(dimensions).map(([key, item]) => (
            <button
              type="button"
              className={dimension === key ? "selected" : ""}
              onClick={() => setDimension(key)}
              key={key}
            >
              {item.label}
            </button>
          ))}
        </div>

        <div className="statistics-list">
          {current.rows.slice(0, 10).map((item) => (
            <div className="statistics-row" key={item.store_id || item.product_id || item.category}>
              <div className="statistics-label">
                <strong>{item[current.nameKey]}</strong>
                <span>¥{formatNumber(item.total_sales)}</span>
              </div>
              <div className="statistics-track">
                <div
                  className="statistics-fill"
                  style={{
                    width: `${Number(item.total_sales) / maxSales * 100}%`
                  }}
                ></div>
              </div>
              <span className="statistics-share">
                {formatNumber(item.sales_share, 2)}%
              </span>
            </div>
          ))}
          {!current.rows.length && (
            <div className="management-empty">当前筛选暂无统计数据</div>
          )}
        </div>
      </section>
    </>
  )
}


export function ToolsPage({
  onOpenAI,
  onRefresh,
  formatNumber
}) {
  const [revenue, setRevenue] = useState("")
  const [orders, setOrders] = useState("")
  const [previous, setPrevious] = useState("")
  const [current, setCurrent] = useState("")
  const aov = Number(orders) > 0
    ? Number(revenue) / Number(orders)
    : null
  const growth = Number(previous) !== 0 && previous !== ""
    ? (Number(current) - Number(previous)) / Number(previous) * 100
    : null

  return (
    <>
      <section className="panel management-hero">
        <div>
          <span className="management-eyebrow">TOOLS</span>
          <h2>经营工具</h2>
          <p>使用本地计算器验证客单价与环比，不会写入经营数据库。</p>
        </div>
        <div className="management-actions">
          <button type="button" onClick={onRefresh}>刷新经营数据</button>
          <button type="button" className="primary" onClick={onOpenAI}>打开 AI 助手</button>
        </div>
      </section>

      <section className="tool-grid">
        <article className="panel calculator-card">
          <h3>客单价计算器</h3>
          <label>
            <span>营业额</span>
            <input
              type="number"
              min="0"
              value={revenue}
              onChange={(event) => setRevenue(event.target.value)}
              placeholder="例如 10000"
            />
          </label>
          <label>
            <span>订单量</span>
            <input
              type="number"
              min="0"
              value={orders}
              onChange={(event) => setOrders(event.target.value)}
              placeholder="例如 250"
            />
          </label>
          <div className="calculator-result">
            <span>计算结果</span>
            <strong>{aov === null ? "--" : `¥${formatNumber(aov, 2)}`}</strong>
          </div>
          <button type="button" onClick={() => { setRevenue(""); setOrders("") }}>
            清空
          </button>
        </article>

        <article className="panel calculator-card">
          <h3>环比计算器</h3>
          <label>
            <span>上期数值</span>
            <input
              type="number"
              value={previous}
              onChange={(event) => setPrevious(event.target.value)}
              placeholder="例如 8000"
            />
          </label>
          <label>
            <span>本期数值</span>
            <input
              type="number"
              value={current}
              onChange={(event) => setCurrent(event.target.value)}
              placeholder="例如 10000"
            />
          </label>
          <div className="calculator-result">
            <span>变化率</span>
            <strong>
              {growth === null
                ? "--"
                : `${growth > 0 ? "+" : ""}${formatNumber(growth, 2)}%`}
            </strong>
          </div>
          <button type="button" onClick={() => { setPrevious(""); setCurrent("") }}>
            清空
          </button>
        </article>
      </section>
    </>
  )
}


export function DataCenterPage({
  analytics,
  loading,
  error,
  onRefresh,
  formatNumber
}) {
  const [view, setView] = useState("overview")
  const summary = analytics?.summary || {}
  const filters = analytics?.filters || {}

  const exportJson = () => {
    downloadTextFile(
      "经营数据快照.json",
      JSON.stringify(analytics || {}, null, 2),
      "application/json;charset=utf-8"
    )
  }

  return (
    <>
      <section className="panel management-hero">
        <div>
          <span className="management-eyebrow">DATA CENTER</span>
          <h2>数据中心</h2>
          <p>检查当前数据范围、维度数量及前端使用的只读字段契约。</p>
        </div>
        <div className="management-actions">
          <button type="button" onClick={onRefresh} disabled={loading}>重新同步</button>
          <button type="button" onClick={exportJson} disabled={!analytics}>导出 JSON</button>
        </div>
      </section>

      <section className="panel management-panel">
        <div className="management-tabs">
          <button
            type="button"
            className={view === "overview" ? "selected" : ""}
            onClick={() => setView("overview")}
          >
            数据概览
          </button>
          <button
            type="button"
            className={view === "schema" ? "selected" : ""}
            onClick={() => setView("schema")}
          >
            字段说明
          </button>
        </div>

        {view === "overview" ? (
          <div className="data-source-grid">
            <article>
              <span>销售事实</span>
              <strong>¥{formatNumber(summary.total_sales)}</strong>
              <small>{formatNumber(summary.order_count)} 个去重订单</small>
            </article>
            <article>
              <span>门店维度</span>
              <strong>{formatNumber(filters.stores?.length)} 家</strong>
              <small>{formatNumber(filters.categories?.length)} 个品类</small>
            </article>
            <article>
              <span>商品维度</span>
              <strong>{formatNumber(filters.products?.length)} 个</strong>
              <small>SQLite products</small>
            </article>
            <article>
              <span>同步状态</span>
              <strong>{loading ? "同步中" : error ? "异常" : "正常"}</strong>
              <small>{error || `更新至 ${analytics?.latest_data_date || "--"}`}</small>
            </article>
          </div>
        ) : (
          <div className="schema-list">
            <div><strong>summary</strong><span>营业额、订单量、客单价、销量、领先维度</span></div>
            <div><strong>trend</strong><span>最近三个月的经营指标序列</span></div>
            <div><strong>product_ranking</strong><span>商品销售、订单、销量及占比</span></div>
            <div><strong>store_ranking</strong><span>门店、品类、区域及经营指标</span></div>
            <div><strong>category_ranking</strong><span>品类贡献及销售占比</span></div>
          </div>
        )}
      </section>
    </>
  )
}


export function HelpPanel({
  open,
  onClose
}) {
  const [query, setQuery] = useState("")
  const topics = [
    ["全局筛选", "选择门店、品类或商品后，首页、销售、商品、报表和统计会使用同一筛选结果。"],
    ["时间范围", "最新月查看最近完整数据月；近3月将汇总最近三个数据月。"],
    ["AI 助手", "AI 会话独立保存在浏览器本地，可通过新会话按钮清空。"],
    ["导出报表", "我的报表支持按当前筛选导出 CSV，数据中心支持导出 JSON。"],
  ]
  const visibleTopics = topics.filter((topic) => (
    !query
    || `${topic[0]}${topic[1]}`.includes(query)
  ))

  if (!open) {
    return null
  }

  return (
    <div className="utility-mask" onClick={onClose}>
      <section
        className="utility-dialog help-dialog"
        onClick={(event) => event.stopPropagation()}
      >
        <header>
          <div>
            <h3>帮助中心</h3>
            <span>经营分析工作台使用说明</span>
          </div>
          <button type="button" onClick={onClose}>×</button>
        </header>
        <input
          className="help-search"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="搜索帮助主题"
        />
        <div className="help-topic-list">
          {visibleTopics.map(([title, content]) => (
            <article key={title}>
              <strong>{title}</strong>
              <p>{content}</p>
            </article>
          ))}
          {!visibleTopics.length && (
            <div className="management-empty">没有匹配的帮助主题</div>
          )}
        </div>
      </section>
    </div>
  )
}


export function NotificationsPanel({
  open,
  onClose
}) {
  const [read, setRead] = useState([])
  const notices = [
    ["data", "经营数据已更新", "最新数据已同步至 2026-07-31"],
    ["report", "门店报表可用", "现在可以按筛选条件导出门店与商品报表"],
    ["ai", "AI 助手已就绪", "可继续使用当前本地会话上下文"],
  ]

  if (!open) {
    return null
  }

  return (
    <div className="topbar-popover notification-popover">
      <header>
        <strong>通知</strong>
        <button type="button" onClick={() => setRead(notices.map(([id]) => id))}>
          全部已读
        </button>
      </header>
      {notices.map(([id, title, content]) => (
        <button
          type="button"
          className={`notification-item ${read.includes(id) ? "read" : ""}`}
          onClick={() => setRead((current) => current.includes(id) ? current : [...current, id])}
          key={id}
        >
          <span className="notification-dot"></span>
          <span>
            <strong>{title}</strong>
            <small>{content}</small>
          </span>
        </button>
      ))}
      <button type="button" className="popover-close" onClick={onClose}>关闭</button>
    </div>
  )
}


export function ProfileMenu({
  open,
  onSettings,
  onNewSession,
  onClose
}) {
  if (!open) {
    return null
  }

  return (
    <div className="topbar-popover profile-popover">
      <div className="profile-summary">
        <div className="avatar">M</div>
        <div>
          <strong>管理员</strong>
          <span>经营分析工作台</span>
        </div>
      </div>
      <button type="button" onClick={onSettings}>界面设置</button>
      <button type="button" onClick={onNewSession}>开始新 AI 会话</button>
      <button type="button" onClick={onClose}>关闭菜单</button>
    </div>
  )
}


export function SettingsDrawer({
  open,
  settings,
  onChange,
  onClose
}) {
  if (!open) {
    return null
  }

  return (
    <>
      <div className="utility-mask settings-mask" onClick={onClose}></div>
      <aside className="settings-drawer">
        <header>
          <div>
            <h3>界面设置</h3>
            <span>设置仅保存在当前浏览器</span>
          </div>
          <button type="button" onClick={onClose}>×</button>
        </header>
        <label className="settings-row">
          <span>
            <strong>紧凑模式</strong>
            <small>减少面板间距，提高信息密度</small>
          </span>
          <input
            type="checkbox"
            checked={settings.compact}
            onChange={(event) => onChange("compact", event.target.checked)}
          />
        </label>
        <label className="settings-row">
          <span>
            <strong>界面动画</strong>
            <small>启用抽屉和图表过渡效果</small>
          </span>
          <input
            type="checkbox"
            checked={settings.animations}
            onChange={(event) => onChange("animations", event.target.checked)}
          />
        </label>
      </aside>
    </>
  )
}
