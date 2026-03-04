#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

KB_JSON = Path('/home/ubuntu/.openclaw/kb/20_Inbox/todo-list.json')
KB_MD = Path('/home/ubuntu/.openclaw/kb/20_Inbox/todo-list.md')


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_store():
    KB_JSON.parent.mkdir(parents=True, exist_ok=True)
    if not KB_JSON.exists():
        data = {"next_id": 1, "items": []}
        KB_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        render_md(data)


def load_data():
    ensure_store()
    return json.loads(KB_JSON.read_text(encoding='utf-8'))


def save_data(data):
    KB_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    render_md(data)


def render_md(data):
    lines = [
        '# Todo List',
        '',
        f'- Updated: {now_iso()}',
        f'- Total: {len(data["items"])}',
        f'- Open: {sum(1 for i in data["items"] if i["status"] == "open")}',
        f'- Done: {sum(1 for i in data["items"] if i["status"] == "done")}',
        ''
    ]

    open_items = [i for i in data['items'] if i['status'] == 'open']
    done_items = [i for i in data['items'] if i['status'] == 'done']

    lines.append('## Open')
    if not open_items:
        lines.append('- (empty)')
    for i in open_items:
        due = f" | due: {i['due']}" if i.get('due') else ''
        tags = f" | tags: {', '.join(i.get('tags', []))}" if i.get('tags') else ''
        lines.append(f"- [ ] #{i['id']} {i['title']}{due}{tags}")

    lines.append('')
    lines.append('## Done')
    if not done_items:
        lines.append('- (empty)')
    for i in done_items:
        done_at = f" | done: {i['done_at']}" if i.get('done_at') else ''
        lines.append(f"- [x] #{i['id']} {i['title']}{done_at}")

    KB_MD.write_text('\n'.join(lines).strip() + '\n', encoding='utf-8')


def cmd_add(args):
    data = load_data()
    item = {
        'id': data['next_id'],
        'title': args.title.strip(),
        'status': 'open',
        'tags': [t.strip() for t in (args.tags or '').split(',') if t.strip()],
        'due': args.due,
        'created_at': now_iso(),
        'updated_at': now_iso(),
        'done_at': None,
        'note': args.note or ''
    }
    data['items'].append(item)
    data['next_id'] += 1
    save_data(data)
    print(f"✅ added #{item['id']}: {item['title']}")


def find_item(data, item_id):
    for i in data['items']:
        if i['id'] == item_id:
            return i
    return None


def cmd_list(args):
    data = load_data()
    items = data['items']
    if args.status != 'all':
        items = [i for i in items if i['status'] == args.status]
    if args.q:
        q = args.q.lower()
        items = [i for i in items if q in i['title'].lower() or q in i.get('note', '').lower()]

    if not items:
        print('(empty)')
        return

    for i in items:
        mark = '✅' if i['status'] == 'done' else '⬜'
        due = f" | due:{i['due']}" if i.get('due') else ''
        tags = f" | tags:{','.join(i.get('tags', []))}" if i.get('tags') else ''
        print(f"{mark} #{i['id']} {i['title']}{due}{tags}")


def cmd_done(args):
    data = load_data()
    item = find_item(data, args.id)
    if not item:
        print(f"❌ not found: #{args.id}")
        return
    item['status'] = 'done'
    item['done_at'] = now_iso()
    item['updated_at'] = now_iso()
    save_data(data)
    print(f"✅ done #{item['id']}: {item['title']}")


def cmd_reopen(args):
    data = load_data()
    item = find_item(data, args.id)
    if not item:
        print(f"❌ not found: #{args.id}")
        return
    item['status'] = 'open'
    item['done_at'] = None
    item['updated_at'] = now_iso()
    save_data(data)
    print(f"🔁 reopened #{item['id']}: {item['title']}")


def cmd_remove(args):
    data = load_data()
    before = len(data['items'])
    data['items'] = [i for i in data['items'] if i['id'] != args.id]
    if len(data['items']) == before:
        print(f"❌ not found: #{args.id}")
        return
    save_data(data)
    print(f"🗑 removed #{args.id}")


def cmd_update(args):
    data = load_data()
    item = find_item(data, args.id)
    if not item:
        print(f"❌ not found: #{args.id}")
        return
    if args.title:
        item['title'] = args.title.strip()
    if args.note is not None:
        item['note'] = args.note
    if args.tags is not None:
        item['tags'] = [t.strip() for t in args.tags.split(',') if t.strip()]
    if args.due is not None:
        item['due'] = args.due
    item['updated_at'] = now_iso()
    save_data(data)
    print(f"✏️ updated #{item['id']}: {item['title']}")


def main():
    p = argparse.ArgumentParser(description='Todo list stored in KB')
    sp = p.add_subparsers(dest='cmd', required=True)

    p_add = sp.add_parser('add')
    p_add.add_argument('title')
    p_add.add_argument('--tags', default='')
    p_add.add_argument('--due')
    p_add.add_argument('--note')
    p_add.set_defaults(func=cmd_add)

    p_list = sp.add_parser('list')
    p_list.add_argument('--status', choices=['all', 'open', 'done'], default='open')
    p_list.add_argument('--q')
    p_list.set_defaults(func=cmd_list)

    p_done = sp.add_parser('done')
    p_done.add_argument('id', type=int)
    p_done.set_defaults(func=cmd_done)

    p_reopen = sp.add_parser('reopen')
    p_reopen.add_argument('id', type=int)
    p_reopen.set_defaults(func=cmd_reopen)

    p_remove = sp.add_parser('remove')
    p_remove.add_argument('id', type=int)
    p_remove.set_defaults(func=cmd_remove)

    p_update = sp.add_parser('update')
    p_update.add_argument('id', type=int)
    p_update.add_argument('--title')
    p_update.add_argument('--note')
    p_update.add_argument('--tags')
    p_update.add_argument('--due')
    p_update.set_defaults(func=cmd_update)

    args = p.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
