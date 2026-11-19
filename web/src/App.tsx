import { useEffect, useMemo, useState, type ReactNode } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import * as Tabs from '@radix-ui/react-tabs';
import {
  ArrowDownToLine, Box, Check, CheckCircle2, ChevronDown, CircleHelp,
  Copy, ExternalLink, Github, Grid3X3, Info, Layers3, LayoutGrid, LoaderCircle,
  Menu, Moon, Move3D, Orbit, Pause, Play, RotateCcw, Ruler, Search,
  Settings2, ShieldCheck, SlidersHorizontal, Sun, X, type LucideIcon,
} from 'lucide-react';
import ModelViewer, { type ViewDirection } from './components/ModelViewer';
import HookConfigurator from './components/HookConfigurator';
import { assetUrl, formatLength, repoUrl, workflowUrl, type Category, type StudioCatalog, type StudioModel } from './data/types';

type Filter = 'All' | Category;
type PanelTab = 'details' | 'customize' | 'files';
const filters: Filter[] = ['All', 'Accessories', 'Connectors', 'Prototypes'];

function getInitialPart(): string | null {
  return new URLSearchParams(window.location.search).get('part');
}
function metric(n: number): string {
  return Number.isInteger(n) ? String(n) : n.toFixed(2);
}

function Logo({ compact = false }: { compact?: boolean }) {
  return (
    <div className="brand" aria-label="openGrid Studio">
      <span className="brand-mark" aria-hidden="true"><svg viewBox="0 0 40 40" width="26" height="26"><path d="M20 3 34.5 11.5v17L20 37 5.5 28.5v-17L20 3Z"/><path d="M5.5 11.5 20 20l14.5-8.5M20 20v17"/><path d="m12 15 15-8.2"/></svg></span>
      {!compact && <span className="brand-text">openGrid <strong>Studio</strong><small>PHYSICAL DESIGN LIBRARY</small></span>}
    </div>
  );
}

function IconButton({ icon: Icon, title, onClick, active = false, disabled = false }: {
  icon: LucideIcon; title: string; onClick: () => void; active?: boolean; disabled?: boolean;
}) {
  return <button className={`tool-button ${active ? 'is-active' : ''}`} type="button" title={title} aria-label={title} aria-pressed={active} onClick={onClick} disabled={disabled}><Icon size={18} strokeWidth={1.7} /></button>;
}

function ModelCard({ model, active, onClick }: { model: StudioModel; active: boolean; onClick: () => void }) {
  return (
    <button type="button" onClick={onClick} aria-pressed={active} className={`model-card ${active ? 'model-card-selected' : ''}`}>
      <span className="model-card-image"><img src={assetUrl(model.preview)} alt="" loading="lazy" /></span>
      <span className="model-card-body"><strong>{model.name}</strong><span>{model.tagline}</span><small><span className="mini-status-dot" /> CAD checked</small></span>
      <span className="card-chevron" aria-hidden="true">›</span>
    </button>
  );
}

function CatalogPanel({ models, selectedId, onSelect, compact = false }: {
  models: StudioModel[]; selectedId: string; onSelect: (id: string) => void; compact?: boolean;
}) {
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState<Filter>('All');
  const matching = useMemo(() => models.filter(m => (filter === 'All' || m.type === filter) &&
    `${m.name} ${m.type} ${m.tagline} ${m.tags.join(' ')}`.toLowerCase().includes(query.toLowerCase())), [models, filter, query]);
  return (
    <div className={`catalog-panel ${compact ? 'compact-catalog' : ''}`}>
      <div className="catalog-header"><div><div className="eyebrow">YOUR WORKSPACE</div><h2>Component library <span className="count-pill">{models.length}</span></h2></div></div>
      <label className="search-field"><Search size={16} strokeWidth={1.8} /><input type="search" value={query} onChange={e => setQuery(e.currentTarget.value)} placeholder="Find a component" aria-label="Search components" />{query && <button type="button" className="clear-search" title="Clear search" onClick={() => setQuery('')}><X size={15}/></button>}</label>
      <div className="filter-row" role="group" aria-label="Filter by component type">
        {filters.map(f => <button key={f} type="button" className={`filter-chip ${filter === f ? 'selected' : ''}`} onClick={() => setFilter(f)} aria-pressed={filter === f}>{f}</button>)}
      </div>
      <div className="model-list" role="list" aria-label="Available CAD components">
        {matching.length > 0 ? matching.map(model => <ModelCard key={model.id} model={model} active={model.id === selectedId} onClick={() => onSelect(model.id)} />)
          : <div className="empty-catalog"><Search size={26}/><strong>No matching parts</strong><span>Try a different keyword or category.</span><button className="text-button" onClick={() => { setQuery(''); setFilter('All'); }}>Clear filters</button></div>}
      </div>
      <div className="catalog-footer"><Layers3 size={16}/><span>One library. Reusable geometry.</span></div>
    </div>
  );
}

function Status({ verified, label }: { verified: boolean; label: string }) {
  return <div className={`check-row ${verified ? 'check-passed' : ''}`}>{verified ? <CheckCircle2 size={16}/> : <span className="unchecked-circle"/>}<span>{label}</span><strong>{verified ? 'Passed' : 'Pending'}</strong></div>;
}

function FileDownloads({ model }: { model: StudioModel }) {
  const entries = Object.entries(model.downloads).sort((a, b) => a[0] === 'STEP' ? -1 : b[0] === 'STEP' ? 1 : 0);
  return (
    <div className="files-list">
      <div className="section-heading-row"><h3>Manufacturing files</h3><span className="count-pill">{entries.length}</span></div>
      <p className="panel-subtitle">Original generated files for your CAD tools or slicer.</p>
      {entries.map(([format, path]) => <a className="download-row" href={assetUrl(path)} download key={format}>
        <span className="file-icon"><Box size={18}/></span><span className="download-detail"><strong>{format}</strong><span>{format === 'STEP' ? 'Editable CAD geometry' : format === '3MF' ? 'Printable mesh package' : 'Triangle mesh for slicing'}</span></span><ArrowDownToLine size={18}/>
      </a>)}
      <a className="download-row" href={assetUrl(model.model)} download><span className="file-icon"><Move3D size={18}/></span><span className="download-detail"><strong>GLB</strong><span>Browser-compatible 3D model</span></span><ArrowDownToLine size={18}/></a>
      <div className="info-line"><Info size={15}/><span>Files are CAD-checked. Slicer and physical fit testing are still required.</span></div>
    </div>
  );
}

function ModelInspector({ model, tab, setTab, notify }: {
  model: StudioModel;
  tab: PanelTab;
  setTab: (t: PanelTab) => void;
  notify: (s: string) => void;
}) {
  const bounds = model.boundsInches;
  return (
    <div className="inspector">
      <div className="inspector-top"><div className="eyebrow">SELECTED COMPONENT</div><h2>{model.name}</h2><p>{model.tagline}</p><div className="pill-pair"><span className="type-pill">{model.type}</span><span className="verified-pill"><Check size={13} /> CAD geometry passed</span></div></div>
      <Tabs.Root className="inspector-tabs" value={tab} onValueChange={v => setTab(v as PanelTab)}>
        <Tabs.List className="tabs-list" aria-label="Component details">
          <Tabs.Trigger value="details">Details</Tabs.Trigger>
          <Tabs.Trigger value="customize">Customize</Tabs.Trigger>
          <Tabs.Trigger value="files">Files</Tabs.Trigger>
        </Tabs.List>
        <div className="inspector-scroll">
          <Tabs.Content value="details">
            <div className="detail-section"><h3>About this design</h3><p className="description-text">{model.description}</p></div>
            <div className="detail-section"><h3>Dimensions</h3><div className="dimension-cards"><div><span>Width</span><strong>{formatLength(bounds[0])}</strong></div><div><span>Depth</span><strong>{formatLength(bounds[1])}</strong></div><div><span>Height</span><strong>{formatLength(bounds[2])}</strong></div></div><p className="small-note">Bounding-box measurements from the actual CAD mesh.</p></div>
            <div className="detail-section"><h3>Engineering status</h3><Status verified={model.validation.cadValid} label="CAD geometry"/><Status verified={model.validation.meshWatertight} label="Watertight mesh"/><Status verified={model.validation.slicerVerified} label="Slicer checked"/><Status verified={model.validation.fitVerified} label="Physical fit"/><Status verified={model.validation.loadTested} label="Load tested"/></div>
            <div className="detail-section"><h3>Interface & source</h3><div className="metadata-grid"><span>Connection</span><strong>{model.interface}</strong><span>Original geometry</span><strong>{model.provenance}</strong><span>Material</span><strong>{model.material}</strong><span>Triangles</span><strong>{model.triangles.toLocaleString()}</strong><span>Volume</span><strong>{metric(model.volumeCubicInches)} in³</strong></div></div>
            <a className="source-link" href={`${repoUrl}/blob/main/${model.source}`} target="_blank" rel="noopener noreferrer">View source file on GitHub <ExternalLink size={14}/></a>
          </Tabs.Content>
          <Tabs.Content value="customize">
            {model.id === 'og-cable-hook-v1' ? <HookConfigurator key={model.id} modelId={model.id} notify={notify} /> : <div className="unavailable"><Settings2 size={30}/><h3>Parametric controls</h3><p>This component's geometry is displayed from a validated CAD export. Browser-based parameter editing isn't available for this design yet.</p><a href={workflowUrl} target="_blank" rel="noopener noreferrer" className="secondary-action">Open CAD workflow <ExternalLink size={14}/></a></div>}
          </Tabs.Content>
          <Tabs.Content value="files"><FileDownloads model={model}/></Tabs.Content>
        </div>
      </Tabs.Root>
      <div className="inspector-bottom"><button className="primary-action full" type="button" onClick={() => setTab('files')}><ArrowDownToLine size={17}/> Get CAD files</button></div>
    </div>
  );
}

function ViewerToolbar({ wireframe, setWireframe, grid, setGrid, rotating, setRotating, view, setView, reset, notify }: {
  wireframe: boolean; setWireframe: (b: boolean) => void;
  grid: boolean; setGrid: (b: boolean) => void;
  rotating: boolean; setRotating: (b: boolean) => void;
  view: ViewDirection; setView: (v: ViewDirection) => void;
  reset: () => void; notify: (s: string) => void;
}) {
  return <div className="viewer-toolbar" role="toolbar" aria-label="3D viewer controls">
    <div className="toolbar-group"><IconButton icon={RotateCcw} title="Reset camera" onClick={reset}/><IconButton icon={Grid3X3} title="Toggle reference grid" active={grid} onClick={() => setGrid(!grid)}/><IconButton icon={Layers3} title="Toggle wireframe" active={wireframe} onClick={() => setWireframe(!wireframe)}/><IconButton icon={rotating ? Pause : Play} title={rotating ? 'Stop auto-rotate' : 'Auto-rotate model'} active={rotating} onClick={() => setRotating(!rotating)}/></div>
    <span className="toolbar-separator"/>
    <div className="view-selector"><label htmlFor="view-orientation" className="sr-only">View orientation</label><select value={view} onChange={e => setView(e.currentTarget.value as ViewDirection)} id="view-orientation" title="Set camera orientation"><option value="iso">Isometric</option><option value="top">Top</option><option value="front">Front</option><option value="right">Side</option></select><ChevronDown size={14}/></div>
    <IconButton icon={Copy} title="Copy model link" onClick={() => { void navigator.clipboard.writeText(window.location.href).then(() => notify('Link copied'), () => notify('Could not copy link')); }} />
  </div>;
}

function CatalogLoading({ failure, retry }: { failure: string | null; retry: () => void }) {
  return <main className="load-screen"><Logo/><div className="loading-card">{failure ? <><Info size={28}/><h2>Couldn't load the CAD catalog</h2><p>{failure}</p><button type="button" className="primary-action" onClick={retry}>Try again</button></> : <><LoaderCircle className="spin" size={30}/><h2>Preparing your workspace</h2><p>Loading CAD geometry and component data…</p></>}</div><a href={repoUrl} target="_blank" rel="noopener noreferrer">View source on GitHub <ExternalLink size={13}/></a></main>;
}

function Modal({ open, onChange, children, title }: { open: boolean; onChange: (b: boolean) => void; children: ReactNode; title: string }) {
  return <Dialog.Root open={open} onOpenChange={onChange}><Dialog.Portal><Dialog.Overlay className="dialog-overlay"/><Dialog.Content className="dialog-content"><div className="dialog-header"><Dialog.Title>{title}</Dialog.Title><Dialog.Close className="icon-button" aria-label="Close dialog"><X size={20}/></Dialog.Close></div>{children}</Dialog.Content></Dialog.Portal></Dialog.Root>;
}

export default function App() {
  const [catalog, setCatalog] = useState<StudioCatalog | null>(null);
  const [loadingError, setLoadingError] = useState<string | null>(null);
  const [retryNumber, setRetryNumber] = useState(0);
  const [selectedId, setSelectedId] = useState(getInitialPart);
  const [tab, setTab] = useState<PanelTab>('details');
  const [wireframe, setWireframe] = useState(false);
  const [grid, setGrid] = useState(true);
  const [rotating, setRotating] = useState(false);
  const [view, setView] = useState<ViewDirection>('iso');
  const [resetVersion, setResetVersion] = useState(0);
  const [viewerError, setViewerError] = useState<string | null>(null);
  const [catalogOpen, setCatalogOpen] = useState(false);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [aboutOpen, setAboutOpen] = useState(false);
  const [toast, setToast] = useState('');
  const [lightMode, setLightMode] = useState(() => window.localStorage.getItem('og-theme') === 'light');

  useEffect(() => {
    const controller = new AbortController();
    setLoadingError(null);
    fetch(assetUrl('catalog.json'), { signal: controller.signal })
      .then(async response => { if (!response.ok) throw new Error(`HTTP ${response.status}. Check the latest GitHub Actions build.`); return (await response.json()) as StudioCatalog; })
      .then(data => {
        if (!data.models || !Array.isArray(data.models) || data.models.length === 0) throw new Error('The component catalog is empty.');
        setCatalog(data);
        setSelectedId(id => id && data.models.some(m => m.id === id) ? id : data.models[0].id);
      }).catch(error => { if (error instanceof Error && error.name !== 'AbortError') setLoadingError(error.message); });
    return () => controller.abort();
  }, [retryNumber]);
  useEffect(() => {
    document.documentElement.dataset.theme = lightMode ? 'light' : 'dark';
    window.localStorage.setItem('og-theme', lightMode ? 'light' : 'dark');
  }, [lightMode]);
  useEffect(() => {
    if (!toast) return;
    const timer = window.setTimeout(() => setToast(''), 3000);
    return () => window.clearTimeout(timer);
  }, [toast]);

  const model = useMemo(() => catalog?.models.find(m => m.id === selectedId) ?? catalog?.models[0] ?? null, [catalog, selectedId]);
  function select(id: string) {
    setSelectedId(id);
    setTab('details');
    setView('iso');
    setWireframe(false);
    setRotating(false);
    setViewerError(null);
    setResetVersion(old => old + 1);
    setCatalogOpen(false);
    const url = new URL(window.location.href);
    url.searchParams.set('part', id);
    window.history.replaceState({}, '', url);
  }
  if (!catalog || !model) return <CatalogLoading failure={loadingError} retry={() => setRetryNumber(x => x + 1)}/>;
  return <div className="studio-shell">
    <header className="topbar">
      <button type="button" className="mobile-menu icon-button" aria-label="Open component library" onClick={() => setCatalogOpen(true)}><Menu size={21}/></button>
      <Logo/>
      <span className="topbar-divider"/>
      <span className="breadcrumb">Workspace <span>/</span> <strong>{model.name}</strong></span>
      <div className="topbar-spacer"/>
      <span className="topbar-build"><span className="success-dot"/> Build verified</span>
      <button type="button" className="icon-button topbar-icon" title="About this studio" aria-label="About openGrid Studio" onClick={() => setAboutOpen(true)}><CircleHelp size={19}/></button>
      <button type="button" className="icon-button topbar-icon" aria-label={lightMode ? 'Use dark theme' : 'Use light theme'} title="Toggle color theme" onClick={() => setLightMode(v => !v)}>{lightMode ? <Moon size={19}/> : <Sun size={19}/>}</button>
      <a href={repoUrl} className="github-button" target="_blank" rel="noopener noreferrer"><Github size={17}/><span>GitHub</span><ExternalLink size={13}/></a>
    </header>
    <div className="workspace-main">
      <aside className="library-sidebar"><CatalogPanel models={catalog.models} selectedId={model.id} onSelect={select}/></aside>
      <main className="viewer-panel">
        <div className="viewer-topline"><div className="eyebrow">3D DESIGN WORKSPACE <span className="eyebrow-separator">/</span> {model.type.toUpperCase()}</div><span className="viewer-revision">REVISION {catalog.generatedFrom.slice(0, 7)}</span></div>
        <div className="viewer-title"><div><h1>{model.name}</h1><p>{model.tagline}</p></div><button type="button" className="mobile-inspector-link secondary-action" onClick={() => setDetailsOpen(true)}><SlidersHorizontal size={16}/> Details</button></div>
        <div className="viewer-stage">
          {viewerError ? <div className="viewer-failure"><Info size={30}/><strong>3D preview unavailable</strong><p>The validated model file is still available for download. {viewerError}</p><button type="button" className="secondary-action" onClick={() => { setViewerError(null); setResetVersion(x => x + 1); }}>Retry 3D view</button></div> :
            <ModelViewer model={model} wireframe={wireframe} grid={grid} rotating={rotating} view={view} resetVersion={resetVersion} lightMode={lightMode} onFailure={setViewerError}/>}
          <div className="stage-corner-top"><span className="status-capsule"><span className="success-dot"/> CAD VALID</span></div>
          <div className="axis-label"><span className="axis-y">Y</span><span className="axis-x">X</span><span className="axis-z">Z</span></div>
          <div className="stage-corner-bottom"><span><Orbit size={15}/> Drag to orbit</span><span>Scroll or pinch to zoom</span></div>
        </div>
        <div className="viewer-controls"><ViewerToolbar wireframe={wireframe} setWireframe={setWireframe} grid={grid} setGrid={setGrid} rotating={rotating} setRotating={setRotating} view={view} setView={setView} reset={() => { setView('iso'); setResetVersion(v => v + 1); }} notify={setToast}/><div className="viewer-hint"><ShieldCheck size={16}/> Geometry validated in GitHub Actions</div></div>
        <div className="viewer-bottom"><div className="spec-metric"><Ruler size={17}/><span>Dimensions</span><strong>{model.boundsInches.map(v => v.toFixed(2)).join(' × ')} in</strong></div><div className="spec-metric"><Box size={16}/><span>Interface</span><strong>{model.interface}</strong></div><button type="button" className="bottom-files" onClick={() => { setTab('files'); setDetailsOpen(true); }}><ArrowDownToLine size={16}/> Files <span>{Object.keys(model.downloads).length}</span></button></div>
      </main>
      <aside className="inspector-sidebar"><ModelInspector model={model} tab={tab} setTab={setTab} notify={setToast}/></aside>
    </div>
    <nav className="mobile-nav" aria-label="Mobile workspace navigation"><button type="button" onClick={() => setCatalogOpen(true)}><LayoutGrid size={19}/>Library</button><button type="button" className="nav-selected" onClick={() => { setCatalogOpen(false); setDetailsOpen(false); }}><Box size={19}/>Viewer</button><button type="button" onClick={() => setDetailsOpen(true)}><SlidersHorizontal size={19}/>Details</button></nav>
    <Modal title="Component library" open={catalogOpen} onChange={setCatalogOpen}><CatalogPanel compact models={catalog.models} selectedId={model.id} onSelect={select}/></Modal>
    <Modal title="Component details" open={detailsOpen} onChange={setDetailsOpen}><ModelInspector model={model} tab={tab} setTab={setTab} notify={setToast}/></Modal>
    <Modal title="About openGrid Studio" open={aboutOpen} onChange={setAboutOpen}><div className="about-content"><div className="about-mark"><Logo/></div><h3>A place for physical ideas.</h3><p>Explore real, reproducible CAD exports from the openGrid library. Every model in this viewer was generated from source and passed software geometry checks.</p><div className="about-facts"><div><CheckCircle2 size={17}/> 8 source-generated models</div><div><ShieldCheck size={17}/> 3D geometry validated</div><div><Info size={17}/> Physical fit and load tests pending</div></div><a href={repoUrl} className="secondary-action full" target="_blank" rel="noopener noreferrer">View repository <ExternalLink size={14}/></a></div></Modal>
    {toast && <div className="toast" role="status"><Check size={16}/>{toast}</div>}
  </div>;
}
