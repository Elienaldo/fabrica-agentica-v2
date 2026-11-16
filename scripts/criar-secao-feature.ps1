param(
    [Parameter(Mandatory=$true)][string]$FeatureName,
    [Parameter(Mandatory=$true)][string]$ResultPath
)
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[Text.UTF8Encoding]::new($false)
$Origin='Fábrica Agêntica V2'; $AnchorName='Âncora V2'; $TemporaryName='Nova seção'
$State=[ordered]@{status='EM_ANDAMENTO';stage='precheck';section_name=$null;section_id=$null;last_confirmed_section=$null;position_current_uncertain=$false;creation_attempted=$false;created=$false;name_confirmed=$false;returned=$false;empty_section_persists=$null;empty_section_bot_buttons=$null;anchor_automation_ids=@();events=@()}
$OwnMenu=$false
function Save-State {
    $json=ConvertTo-Json -InputObject $State -Depth 7 -Compress
    if($json.Length -gt 60000){throw 'Relatório excedeu limite interno; nenhum dump UIA permitido'}
    [IO.File]::WriteAllText($ResultPath,$json,[Text.UTF8Encoding]::new($false))
}
function Stage([string]$name){$State.stage=$name;Save-State}
function Note([string]$name){$State.events += $name}
function Key([string]$s){return $s.Normalize([Text.NormalizationForm]::FormC).Trim().ToUpperInvariant()}
function Has-Token($e,[string]$token){return (($e.Current.ClassName -split ' ') -contains $token)}
function One($values,[string]$label){$v=@($values);if($v.Count -ne 1){throw ($label+': esperado único, obtido '+$v.Count)};return $v[0]}
function Wait-Read([scriptblock]$read,[string]$label,[int]$ms=3000){
    $timer=[Diagnostics.Stopwatch]::StartNew()
    do{$v=& $read;if($null -ne $v){return $v};[Threading.Thread]::Sleep(60)}while($timer.ElapsedMilliseconds -lt $ms)
    throw ('Timeout de leitura: '+$label)
}
function Find-TokenNode {
    # Busca pura (sem UIA): percorre a árvore até o token; distingue encontrado, ausente, indisponível e limite.
    param($Root,[scriptblock]$GetChildren,[scriptblock]$GetClass,[string]$Token,[int]$MaxNodes=20000,[int]$MaxDepth=200,[int]$MaxMs=2500,[int]$MinTree=8)
    $timer=[Diagnostics.Stopwatch]::StartNew()
    $stack=[Collections.Generic.Stack[object]]::new();$stack.Push(@($Root,0));$visited=0;$deep=0
    while($stack.Count){
        if($visited -ge $MaxNodes -or $timer.ElapsedMilliseconds -ge $MaxMs){return [pscustomobject]@{Status='limite';Node=$null;Visited=$visited;Depth=$deep;Ms=$timer.ElapsedMilliseconds}}
        $entry=$stack.Pop();$e=$entry[0];$d=[int]$entry[1];$visited++;if($d -gt $deep){$deep=$d}
        if(((([string](& $GetClass $e)) -split ' ') -contains $Token)){return [pscustomobject]@{Status='encontrado';Node=$e;Visited=$visited;Depth=$d;Ms=$timer.ElapsedMilliseconds}}
        $kids=@(& $GetChildren $e)
        if($kids.Count -and $d -ge $MaxDepth){return [pscustomobject]@{Status='limite';Node=$null;Visited=$visited;Depth=$deep;Ms=$timer.ElapsedMilliseconds}}
        for($i=$kids.Count-1;$i -ge 0;$i--){$stack.Push(@($kids[$i],($d+1)))}
    }
    $status='ausente';if($visited -lt $MinTree){$status='indisponivel'}
    return [pscustomobject]@{Status=$status;Node=$null;Visited=$visited;Depth=$deep;Ms=$timer.ElapsedMilliseconds}
}
function Resolve-TokenNode {
    # Repete só ausente/indisponível (árvore ainda montando) dentro de prazo curto; limite falha na hora. Nunca espera sem fim.
    param($Root,[scriptblock]$GetChildren,[scriptblock]$GetClass,[string]$Token,[int]$RetryMs=2000,[int]$SleepMs=150,[int]$MaxNodes=20000,[int]$MaxMs=2500)
    $timer=[Diagnostics.Stopwatch]::StartNew();$tries=0
    while($true){
        $tries++
        $r=Find-TokenNode -Root $Root -GetChildren $GetChildren -GetClass $GetClass -Token $Token -MaxNodes $MaxNodes -MaxMs $MaxMs
        $info=('nós={0}, profundidade={1}, ms={2}, tentativas={3}' -f $r.Visited,$r.Depth,$timer.ElapsedMilliseconds,$tries)
        if($r.Status -eq 'encontrado'){return $r.Node}
        if($r.Status -eq 'limite'){throw ('Sidebar: limite de busca atingido sem localizar ('+$info+')')}
        if($timer.ElapsedMilliseconds -ge $RetryMs){break}
        [Threading.Thread]::Sleep($SleepMs)
    }
    if($r.Status -eq 'indisponivel'){throw ('Sidebar: árvore de acessibilidade indisponível ou rasa ('+$info+')')}
    throw ('Sidebar não localizada na estrutura pública esperada: árvore completa sem o token ('+$info+')')
}
try {
    if($FeatureName -match '[\p{Cc}\p{Cf}]'){throw 'Nome contém controle/formato invisível'}
    $FeatureName=$FeatureName.Replace('/','-').Replace('\','-').Trim().Normalize([Text.NormalizationForm]::FormC)
    if([string]::IsNullOrWhiteSpace($FeatureName) -or (Key $FeatureName) -in @((Key $Origin),(Key $AnchorName),(Key $TemporaryName))){throw 'Nome vazio/reservado'}
    $State.section_name=[string]$FeatureName
    Save-State
    Add-Type -AssemblyName UIAutomationClient
    Add-Type -AssemblyName UIAutomationTypes
    Add-Type -AssemblyName WindowsBase
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class SectionUI {
 [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X; public int Y; }
 [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")] public static extern bool SetCursorPos(int x,int y);
 [DllImport("user32.dll")] public static extern bool GetCursorPos(out POINT p);
 [DllImport("user32.dll")] public static extern void mouse_event(uint f,uint x,uint y,uint d,UIntPtr e);
}
'@
    $RW=[System.Windows.Automation.TreeWalker]::RawViewWalker
    function By-Type($root,$type){return $root.FindAll([System.Windows.Automation.TreeScope]::Descendants,[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ControlTypeProperty,$type))}
    function Main-Window {
        $wins=[System.Windows.Automation.AutomationElement]::RootElement.FindAll([System.Windows.Automation.TreeScope]::Children,[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::NameProperty,'Grok Bot'))
        return (One @($wins|Where-Object{$_.Current.ClassName -ceq 'Chrome_WidgetWin_1' -and $_.Current.ControlType -eq [System.Windows.Automation.ControlType]::Window}) 'Janela Grok Bot')
    }
    $W=Main-Window
    $windowPattern=$W.GetCurrentPattern([System.Windows.Automation.WindowPattern]::Pattern)
    if($windowPattern.Current.WindowVisualState -eq [System.Windows.Automation.WindowVisualState]::Minimized){throw 'App minimizado; não restaurado automaticamente'}
    function Foreground {if([SectionUI]::GetForegroundWindow().ToInt64() -ne $W.Current.NativeWindowHandle){throw 'Janela Grok Bot não está em primeiro plano'}}
    function Sidebar {
        $fresh=Main-Window
        if(-not [System.Windows.Automation.Automation]::Compare($fresh,$W)){throw 'Janela foi substituída; parar'}
        $found=Resolve-TokenNode -Root $W -GetChildren {param($n) $c=$RW.GetFirstChild($n);while($c){$c;$c=$RW.GetNextSibling($c)}} -GetClass {param($n) [string]$n.Current.ClassName} -Token 'sand-agents-sidebar'
        $same=$W.FindAll([System.Windows.Automation.TreeScope]::Descendants,[System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ClassNameProperty,$found.Current.ClassName))
        return (One $same 'Sidebar por classe atual')
    }
    function Headers($side){return @((By-Type $side ([System.Windows.Automation.ControlType]::Button))|Where-Object{Has-Token $_ 'sand-agents-section__header'})}
    function Section($node){$p=$node;for($i=0;$p -and $i -lt 10;$i++){if(Has-Token $p 'sand-agents-section'){return $p};$p=$RW.GetParent($p)};throw 'Ancestral de seção não comprovado'}
    function Header($section){$r=@();$c=$RW.GetFirstChild($section);while($c){if((Has-Token $c 'sand-agents-section__header') -and $c.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button){$r += $c};$c=$RW.GetNextSibling($c)};return (One $r 'Cabeçalho direto da seção')}
    function Anchor($side){return (One @((By-Type $side ([System.Windows.Automation.ControlType]::Button))|Where-Object{$_.Current.Name -ceq $AnchorName -and (Has-Token $_ 'sand-agent-item')}) 'Âncora V2 na sidebar')}
    function Bots($section){return @((By-Type $section ([System.Windows.Automation.ControlType]::Button))|Where-Object{Has-Token $_ 'sand-agent-item'})}
    function Remember($a,[string]$section){
        $State.last_confirmed_section=[string]$section;$State.position_current_uncertain=$false
        $State.anchor_automation_ids += [string]$a.Current.AutomationId
    }
    function Assert-NameAbsent($side){
        foreach($h in (Headers $side)){
            $name=[string]$h.Current.Name
            if((Key $name) -ceq (Key $FeatureName) -or $name -match ('(?i)^'+[regex]::Escape($FeatureName)+' [0-9]+$')){throw 'Nome destino existente ou legenda agregada potencialmente homônima; nenhuma criação'}
        }
    }
    function Exact-Popup([string]$name,$type){
        $m=@((By-Type $W $type)|Where-Object{$_.Current.Name -ceq $name -and -not $_.Current.IsOffscreen})
        if($m.Count -gt 1){throw ('Popup ambíguo: '+$name)}
        if($m.Count -eq 1){return $m[0]};return $null
    }
    function Select-FreePoint($Rect,$ChildRects,[int]$Margin=2){
        # Pura: ponto dentro da Âncora V2 fora de qualquer filho, para FromPoint devolver a própria Âncora V2. Centro primeiro; depois faixas livres esquerda/direita. Sem ponto livre: $null (falha fechada).
        $cy=[int]($Rect.Y+$Rect.Height/2);$cands=@(,@([int]($Rect.X+$Rect.Width/2),$cy))
        $kids=@($ChildRects|Where-Object{$_ -and $_.Width -gt 0 -and $_.Height -gt 0})
        if($kids.Count){$l=($kids|Measure-Object -Property X -Minimum).Minimum;$r=($kids|ForEach-Object{$_.X+$_.Width}|Measure-Object -Maximum).Maximum;$cands+=,@([int](($Rect.X+$l)/2),$cy);$cands+=,@([int](($r+$Rect.X+$Rect.Width)/2),$cy)}
        foreach($c in $cands){
            $x=$c[0];$y=$c[1]
            if($x -lt $Rect.X+$Margin -or $x -gt $Rect.X+$Rect.Width-$Margin -or $y -lt $Rect.Y+$Margin -or $y -gt $Rect.Y+$Rect.Height-$Margin){continue}
            $inKid=$false;foreach($k in $kids){if($x -ge $k.X-1 -and $x -le $k.X+$k.Width+1 -and $y -ge $k.Y-1 -and $y -le $k.Y+$k.Height+1){$inKid=$true;break}}
            if(-not $inKid){return [pscustomobject]@{X=$x;Y=$y}}
        }
        return $null
    }
    function Set-Pointer($e,$Pt=$null){
        $b=$e.Current.BoundingRectangle
        if($e.Current.IsOffscreen -or -not $e.Current.IsEnabled -or $b.IsEmpty -or $b.Width -le 0 -or $b.Height -le 0){throw 'Controle sem geometria/visibilidade/habilitação'}
        $wb=$W.Current.BoundingRectangle
        if($b.X -lt $wb.X -or $b.Y -lt $wb.Y -or $b.Right -gt $wb.Right -or $b.Bottom -gt $wb.Bottom){throw 'Controle fora da janela'}
        $x=[int]($b.X+$b.Width/2);$y=[int]($b.Y+$b.Height/2)
        if($Pt){$x=[int]$Pt.X;$y=[int]$Pt.Y;if($x -lt $b.X -or $x -gt $b.Right -or $y -lt $b.Y -or $y -gt $b.Bottom){throw 'Ponto fora do controle'}}
        if(-not [SectionUI]::SetCursorPos($x,$y)){throw 'SetCursorPos falhou'}
        $p=[SectionUI+POINT]::new();if(-not [SectionUI]::GetCursorPos([ref]$p) -or $p.X -ne $x -or $p.Y -ne $y){throw 'Posição real do cursor não confirmada'}
    }
    function Open-Context([string]$expected){
        $side=Sidebar;$a=Anchor $side;$h=Header (Section $a)
        if($h.Current.Name -cne $expected){throw 'Âncora V2 não está na seção esperada'}
        if([SectionUI]::GetForegroundWindow().ToInt64() -ne $W.Current.NativeWindowHandle){$a.SetFocus();$null=Wait-Read {if([SectionUI]::GetForegroundWindow().ToInt64() -eq $W.Current.NativeWindowHandle){return $true};return $null} 'foco Grok Bot' 1200}
        Foreground
        $side=Sidebar;$a=Anchor $side;$h=Header (Section $a)
        if($h.Current.Name -cne $expected){throw 'Ancestralidade mudou após foco'}
        $b=$a.Current.BoundingRectangle
        if($a.Current.IsOffscreen -or -not $a.Current.IsEnabled -or $b.IsEmpty){throw 'Âncora V2 não visível/habilitado'}
        $kr=@();$k=$RW.GetFirstChild($a);while($k){$kr+=$k.Current.BoundingRectangle;$k=$RW.GetNextSibling($k)}
        $pt=Select-FreePoint $b $kr
        if(-not $pt){throw ('Point not in Anchor: sem ponto livre de filhos (filhos='+$kr.Count+')')}
        $hit=[System.Windows.Automation.AutomationElement]::FromPoint([System.Windows.Point]::new($pt.X,$pt.Y))
        $ar=[int[]]$a.GetRuntimeId();$hr=[int[]]$hit.GetRuntimeId()
        if(-not ([System.Linq.Enumerable]::SequenceEqual($ar,$hr) -and (($ar -join ',') -ceq ($hr -join ',')) -and [System.Windows.Automation.Automation]::Compare($a,$hit) -and $hit.Current.Name -ceq $AnchorName -and $hit.Current.ControlType -eq [System.Windows.Automation.ControlType]::Button -and $hit.Current.BoundingRectangle.Equals($b))){$rel='outro';$p=$RW.GetParent($hit);for($i=1;$p -and $i -le 6;$i++){if([System.Windows.Automation.Automation]::Compare($p,$a)){$rel='descendente'+$i;break};$p=$RW.GetParent($p)};throw ('Point not in Anchor: guarda estrita falhou (alvo='+$rel+', tipo='+$hit.Current.ControlType.ProgrammaticName+')')}
        Remember $a $expected
        Set-Pointer $a $pt;Foreground
        [SectionUI]::mouse_event(8,0,0,0,[UIntPtr]::Zero);[SectionUI]::mouse_event(16,0,0,0,[UIntPtr]::Zero)
        $script:OwnMenu=$true
    }
    function Hover-Move {
        $m=Wait-Read {Exact-Popup 'Mover para' ([System.Windows.Automation.ControlType]::MenuItem)} 'Mover para'
        Foreground;Set-Pointer $m
        # Sem Invoke/Expand, sem logs/disco/retorno ao launcher entre direito e hover.
        $menu=Wait-Read {Exact-Popup 'Mover para seção' ([System.Windows.Automation.ControlType]::Menu)} 'submenu por hover'
        return $menu
    }
    function Menu-Target($menu,[string]$name,$type){
        return (Wait-Read {$m=@((By-Type $menu $type)|Where-Object{$_.Current.Name -ceq $name -and -not $_.Current.IsOffscreen});if($m.Count -gt 1){throw 'Destino de menu ambíguo'};if($m.Count -eq 1){return $m[0]};return $null} ('item '+$name))
    }
    function Verify-Position([string]$expected){
        return (Wait-Read {
            $side=Sidebar;$m=@((By-Type $side ([System.Windows.Automation.ControlType]::Button))|Where-Object{$_.Current.Name -ceq $AnchorName -and (Has-Token $_ 'sand-agent-item')})
            if($m.Count -gt 1){throw 'Âncora V2 duplicado'}
            if($m.Count -eq 1){$h=Header (Section $m[0]);if($h.Current.Name -ceq $expected){return $m[0]}}
            return $null
        } ('Âncora V2 em '+$expected))
    }
    $side=Sidebar
    if(@(By-Type $W ([System.Windows.Automation.ControlType]::MenuItem)).Count -gt 0){throw 'Menu pré-existente de propriedade desconhecida; não fechar nem reutilizar'}
    if(@(By-Type $side ([System.Windows.Automation.ControlType]::Edit)).Count -gt 0){throw 'Edição de sidebar já em andamento'}
    Assert-NameAbsent $side
    $source=One @((Headers $side)|Where-Object{$_.Current.Name -ceq $Origin}) 'Cabeçalho exato de origem (abrir manualmente se legenda agregada não permitir identificação)'
    $expand=$source.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern)
    if($expand.Current.ExpandCollapseState -eq [System.Windows.Automation.ExpandCollapseState]::Collapsed){
        $State.stage='expand_origin';Save-State
        if($source.Current.IsOffscreen){throw 'Origem fora da área visível; mostrar manualmente'}
        if([SectionUI]::GetForegroundWindow().ToInt64() -ne $W.Current.NativeWindowHandle){$source.SetFocus();$null=Wait-Read {if([SectionUI]::GetForegroundWindow().ToInt64() -eq $W.Current.NativeWindowHandle){return $true};return $null} 'foco no cabeçalho origem' 1200}
        Foreground
        $expand.Expand() # Somente cabeçalho inequívoco de origem, uma vez.
        $null=Wait-Read {if($expand.Current.ExpandCollapseState -eq [System.Windows.Automation.ExpandCollapseState]::Expanded){return $true};return $null} 'origem expandida'
    }
    $a=Verify-Position $Origin;Remember $a $Origin
    Stage 'create_context_hover'
    Assert-NameAbsent (Sidebar)
    Open-Context $Origin
    $menu=Hover-Move
    $create=Menu-Target $menu 'Criar seção' ([System.Windows.Automation.ControlType]::MenuItem)
    Foreground
    if(-not $create.Current.IsEnabled -or $create.Current.IsOffscreen){throw 'Criar seção não acionável'}
    $State.creation_attempted=$true;$State.position_current_uncertain=$true
    $create.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke() # UMA criação.
    $OwnMenu=$false
    Stage 'verify_temporary_inline'
    $edit=Wait-Read {
        $side=Sidebar;$es=@((By-Type $side ([System.Windows.Automation.ControlType]::Edit))|Where-Object{$_.Current.Name -ceq 'Renomear seção' -and (Has-Token $_ 'sand-agent-item__name-input') -and -not $_.Current.IsOffscreen})
        if($es.Count -gt 1){throw 'Edit inline ambíguo'}
        if($es.Count -eq 1){$an=Anchor $side;if(-not [System.Windows.Automation.Automation]::Compare((Section $es[0]),(Section $an))){throw 'Edit não pertence à seção de Âncora V2'};$v=$es[0].GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern);if($v.Current.Value -ceq $TemporaryName){return $es[0]}}
        return $null
    } 'Nova seção e Edit inline com Âncora V2'
    $State.created=$true;Remember (Anchor (Sidebar)) $TemporaryName
    Note 'Criar seção criou imediatamente Nova seção com Âncora V2; Edit Renomear seção focado'
    Stage 'set_inline_name'
    $parent=$RW.GetParent($edit)
    if(-not (Has-Token $parent 'sand-agents-section__header')){throw 'Edit fora do cabeçalho esperado'}
    $children=@();$c=$RW.GetFirstChild($parent);while($c){$children += $c;$c=$RW.GetNextSibling($c)}
    if($children.Count -ne 1 -or -not [System.Windows.Automation.Automation]::Compare($children[0],$edit)){throw 'Interface de confirmação mudou; não adivinhar Enter'}
    Foreground
    if(-not $edit.Current.HasKeyboardFocus -or -not [System.Windows.Automation.Automation]::Compare($edit,[System.Windows.Automation.AutomationElement]::FocusedElement)){throw 'Edit exato não está focado'}
    $value=$edit.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
    if($value.Current.IsReadOnly){throw 'Campo somente leitura'}
    $value.SetValue($FeatureName) # UMA escrita; apenas leituras aguardam atualização.
    $null=Wait-Read {if($value.Current.Value -ceq $FeatureName){return $true};return $null} 'valor inline exato'
    Stage 'confirm_inline_name'
    Foreground
    if(-not $edit.Current.HasKeyboardFocus -or -not [System.Windows.Automation.Automation]::Compare($edit,[System.Windows.Automation.AutomationElement]::FocusedElement)){throw 'Foco mudou antes de Enter'}
    [System.Windows.Forms.SendKeys]::SendWait('{ENTER}') # UMA confirmação, somente Edit comprovado.
    $null=Wait-Read {if(@(By-Type (Sidebar) ([System.Windows.Automation.ControlType]::Edit)).Count -eq 0){return $true};return $null} 'saída da edição'
    $a=Verify-Position $FeatureName;Remember $a $FeatureName;$State.name_confirmed=$true
    Stage 'return_context_hover'
    Open-Context $FeatureName
    $menu=Hover-Move
    $radio=Menu-Target $menu $Origin ([System.Windows.Automation.ControlType]::RadioButton)
    $selection=$radio.GetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern)
    if($selection.Current.IsSelected -or -not $radio.Current.IsEnabled -or $radio.Current.IsOffscreen){throw 'Origem no submenu não acionável'}
    Foreground;$State.position_current_uncertain=$true
    $radio.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke() # UM retorno normal, não rollback.
    $OwnMenu=$false
    Stage 'verify_return'
    $a=Verify-Position $Origin;Remember $a $Origin;$State.returned=$true
    Stage 'verify_empty_section'
    $timer=[Diagnostics.Stopwatch]::StartNew();while($timer.ElapsedMilliseconds -lt 2500){[Threading.Thread]::Sleep(100)}
    $side=Sidebar;$h=One @((Headers $side)|Where-Object{$_.Current.Name -ceq $FeatureName}) 'Seção criada após retorno (não recriar se ausente)'
    $ep=$h.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern)
    if($ep.Current.ExpandCollapseState -ne [System.Windows.Automation.ExpandCollapseState]::Expanded){throw 'Seção destino não expandida; vazio não comprovado'}
    $count=@(Bots (Section $h)).Count
    $State.empty_section_bot_buttons=$count
    if($count -ne 0){throw 'Seção destino não está vazia'}
    $State.empty_section_persists=$true
    $a=Verify-Position $Origin;Remember $a $Origin
    if(@(By-Type $W ([System.Windows.Automation.ControlType]::MenuItem)).Count -ne 0){throw 'Menu inesperado no final'}
    $State.status='CONCLUIDO';$State.stage='done';$State.message='Seção criada; Âncora V2 devolvido; seção vazia permanece nesta sessão. section_id deve ser obtido posteriormente pelo Bootstrapper (ListSections).'
    Save-State
    exit 0
} catch {
    $State.status='ABORTADO';$State.message=[string]$_.Exception.Message
    # Nunca repetir criação, escrita, Enter ou movimento. Nenhum rollback automático.
    # Fechar somente menu do próprio controlador, nunca campo de rename/diálogo desconhecido.
    if($OwnMenu -and $null -ne ('SectionUI' -as [type])){
        try {
            Foreground
            for($i=0;$i -lt 2;$i++){
                $m=Exact-Popup 'Mover para' ([System.Windows.Automation.ControlType]::MenuItem)
                if($null -eq $m){break}
                [System.Windows.Forms.SendKeys]::SendWait('{ESC}')
                [Threading.Thread]::Sleep(80)
            }
        } catch { $State.events += 'Menu não foi fechado com segurança; conferir manualmente' }
    }
    try { Save-State } catch { [Console]::Error.WriteLine('Falha ao salvar relatório; estado da UI deve ser conferido manualmente.') }
    exit 3
}
