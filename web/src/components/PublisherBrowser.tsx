import { useEffect, useMemo, useState } from 'react';
import { ExternalLink, FileText, Search } from 'lucide-react';
import { assetUrl } from '../data/types';

type Source = {
  id: number; title: string; creator: string; license: string;
  collection: string; url: string; files: number; models: number;
};
type FileItem = { id: string; name: string; format: string; bytes: number };
type PublisherModel = {
  sourceId: number; name: string; files: FileItem[];
  legacy: boolean; beta: boolean;
};
type Index = { sources: Source[]; models: PublisherModel[]; totalFiles: number; scope: string };
const LIMIT = 35;

export default function PublisherBrowser({ active }: { active: boolean }) {
  const [index, setIndex] = useState<Index | null>(null);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');
  const [license, setLicense] = useState('all');
  const [source, setSource] = useState('all');
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    if (!active || index) return;
    const controller = new AbortController();
    fetch(assetUrl('publisher-index.json'), { signal: controller.signal })
      .then(async res => {
        if (!res.ok) throw new Error('Published model catalog could not be loaded.');
        return await res.json() as Index;
      })
      .then(setIndex)
      .catch(err => { if (err?.name !== 'AbortError') setError('Publisher catalog unavailable. Try reopening it.'); });
    return () => controller.abort();
  }, [active, index]);

  const results = useMemo(() => {
    if (!index) return [];
    const text = query.trim().toLowerCase();
    return index.models.filter(model => {
      const src = index.sources.find(x => x.id === model.sourceId);
      return src && (source === 'all' || String(src.id) === source)
        && (license === 'all' || src.license === license)
        && (!text || [model.name, src.title, src.creator, ...model.files.map(f => f.name)]
          .join(' ').toLowerCase().includes(text));
    });
  }, [index, query, license, source]);
  useEffect(() => setOffset(0), [query, license, source]);

  if (!index) return <p className="publisher-notice">{error || 'Loading original publisher catalog…'}</p>;
  const sourceMap = new Map(index.sources.map(x => [x.id, x]));
  return <div className="publisher-browser">
    <p className="publisher-notice">Search {index.models.length} published model groups and {index.totalFiles} source files from {index.sources.length} verified releases. Models labeled <strong>Source linked</strong> are indexed with the original publisher, and aren't all stored or rendered in this Studio. The 3D library remains a separate, verified set.</p>
    <div className="publisher-search"><Search size={16}/><input aria-label="Search published models" placeholder="Search models or filenames" value={query} onChange={e => setQuery(e.target.value)}/></div>
    <div className="publisher-filters">
      <label>Collection <select aria-label="Filter publisher" value={source} onChange={e => setSource(e.target.value)}>
        <option value="all">All collections</option>
        {index.sources.map(s => <option key={s.id} value={String(s.id)}>{s.title} ({s.models})</option>)}
      </select></label>
      <label>License <select aria-label="Filter license" value={license} onChange={e => setLicense(e.target.value)}>
        <option value="all">All licenses</option>
        <option value="CC BY 4.0">CC BY 4.0</option>
        <option value="CC BY-SA 4.0">CC BY-SA 4.0</option>
        <option value="CC BY-NC-SA 4.0">CC BY-NC-SA 4.0</option>
      </select></label>
    </div>
    <div className="publisher-result-count">{results.length} matching model groups · Showing {results.length ? offset + 1 : 0} to {Math.min(offset + LIMIT, results.length)}</div>
    <div className="publisher-results">
      {results.slice(offset, offset + LIMIT).map((model,i) => {
        const src = sourceMap.get(model.sourceId)!;
        return <div className="publisher-result" key={model.sourceId + ':' + model.name + ':' + (offset+i)}>
          <div className="publisher-result-heading">
            <strong>{model.name}</strong>
            <span className="publisher-chip">Source linked</span>
          </div>
          <div className="publisher-result-meta">{src.creator} · {src.license} · {src.collection}{model.legacy ? ' · OLD' : ''}{model.beta ? ' · BETA' : ''}</div>
          <div className="publisher-file-formats"><FileText size={14}/>{model.files.map(f => f.format).join(' · ')} · {model.files.length} source {model.files.length === 1 ? 'file' : 'files'}</div>
          <a href={src.url} target="_blank" rel="noopener noreferrer">View published files <ExternalLink size={13}/></a>
        </div>;
      })}
      {!results.length && <p className="publisher-notice">No publisher models matched these filters.</p>}
    </div>
    <div className="publisher-pagination">
      <button type="button" disabled={offset === 0} onClick={() => setOffset(x => Math.max(0, x-LIMIT))}>Previous</button>
      <span>Page {Math.floor(offset/LIMIT)+1} of {Math.max(1,Math.ceil(results.length/LIMIT))}</span>
      <button type="button" disabled={offset + LIMIT >= results.length} onClick={() => setOffset(x => x+LIMIT)}>Next</button>
    </div>
    <p className="publisher-notice">This index records original filenames and source IDs. Download from each creator's published listing; model files have different terms of reuse. Noncommercial and ShareAlike restrictions still apply, including to redistributed files and derivatives.</p>
  </div>;
}
