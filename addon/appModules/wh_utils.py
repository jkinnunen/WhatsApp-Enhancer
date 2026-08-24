from collections import deque

def collect_elements(root, condition, max_items=50):
	if not root:
		return []
	results = []
	queue = deque([root])
	visited = 0
	while queue and visited < max_items:
		obj = queue.popleft()
		visited += 1
		try:
			if condition(obj):
				results.append(obj)
			child = obj.firstChild
			while child:
				queue.append(child)
				child = child.next
		except Exception:
			continue
	return results


def find_element(root, condition, max_items=150):
	if not root:
		return None
	queue = deque([root])
	visited = 0
	while queue and visited < max_items:
		obj = queue.popleft()
		visited += 1
		try:
			child = obj.firstChild
			while child:
				if condition(child):
					return child
				queue.append(child)
				child = child.next
		except Exception:
			continue
	return None
