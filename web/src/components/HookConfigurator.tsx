import { useState } from 'react';
import { ArrowDownToLine, ExternalLink, Info, RotateCcw } from 'lucide-react';
import type { HookParams } from '../data/types';
import { workflowUrl } from '../data/types';

const DEFAULTS: HookParams = { stemLengthIn: 0.75, stemDiameterIn: 0.30, lipDiameterIn: 0.50 };

function NumberControl({ label, value, min, max, step, onChange }: {
  label: string; value: number; min: number; max: number; step: number;
  onChange: (n: number) => void;
}) {
  return (
    <label className="parameter-row">
      <span className="parameter-heading"><span>{label}</span><span className="number-value">{value.toFixed(2)} <small>in</small></span></span>
      <input type="range" min={min} max={max} step={step} value={value} onChange={event => onChange(Number(event.currentTarget.value))} aria-label={`${label} in inches`} />
      <span className="range-extents"><span>{min.toFixed(2)} in</span><span>{max.toFixed(2)} in</span></span>
    </label>
  );
}

export default function HookConfigurator({ modelId, notify }: { modelId: string; notify: (s: string) => void }) {
  const [params, setParams] = useState<HookParams>(DEFAULTS);
  const [mode, setMode] = useState<'default' | 'draft'>('default');
  const set = (field: keyof HookParams, value: number) => {
    setParams(old => {
      const next = { ...old, [field]: value };
      if (next.lipDiameterIn <= next.stemDiameterIn) {
        if (field === 'stemDiameterIn') next.lipDiameterIn = Math.min(0.75, Number((value + 0.05).toFixed(2)));
        else next.lipDiameterIn = Number((next.stemDiameterIn + 0.05).toFixed(2));
      }
      return next;
    });
    setMode('draft');
  };
  const save = () => {
    const spec = {
      schemaVersion: '1.0.0',
      design: modelId,
      generator: 'cad/opengrid/generate_accessory.py',
      parametersInches: params,
      approval: { cadGenerated: false, slicerVerified: false, fitVerified: false },
    };
    const blob = new Blob([JSON.stringify(spec, null, 2) + '\n'], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'opengrid-cable-hook-build-request.json';
    link.click();
    URL.revokeObjectURL(url);
    notify('Build request downloaded');
  };
  return (
    <div className="configurator">
      <div className="section-heading-row"><h3>Parametric settings</h3><button type="button" className="icon-button small" title="Restore defaults" aria-label="Restore default dimensions" onClick={() => { setParams(DEFAULTS); setMode('default'); }}><RotateCcw size={15} /></button></div>
      <p className="panel-subtitle">Edit your cable hook dimensions.</p>
      <NumberControl label="Peg length" min={0.30} max={2} step={0.05} value={params.stemLengthIn} onChange={v => set('stemLengthIn', v)} />
      <NumberControl label="Peg diameter" min={0.18} max={0.50} step={0.01} value={params.stemDiameterIn} onChange={v => set('stemDiameterIn', v)} />
      <NumberControl label="Retaining lip" min={Number((params.stemDiameterIn + 0.05).toFixed(2))} max={0.75} step={0.01} value={params.lipDiameterIn} onChange={v => set('lipDiameterIn', v)} />
      <div className="draft-notice"><Info size={16} /><span>{mode === 'draft' ? 'Draft values only. The 3D view still shows the last generated, CAD-validated model.' : 'Showing the generated default model. Change dimensions to make a build request.'}</span></div>
      <button type="button" onClick={save} className="primary-action full"><ArrowDownToLine size={16} /> Download build request</button>
      <a className="secondary-action full" target="_blank" rel="noopener noreferrer" href={workflowUrl}>Run CAD generator on GitHub <ExternalLink size={14} /></a>
      <p className="helper-text">Open the workflow, choose <strong>Run workflow</strong>, and enter the same dimensions. Download the generated files from that run's Artifacts. Website generation is not real-time.</p>
    </div>
  );
}
